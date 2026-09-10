"""LLM Factory with Multi-Model Fallback Engine.

Provides flexible initialization for Google Gemini and OpenAI models,
with automatic fallback chaining so if the primary LLM fails (rate-limit,
quota exhaustion, invalid model, network error), the fallback model seamlessly takes over.
"""

from typing import List, Optional
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from app.config.settings import settings
from app.utils.logger import logger


def get_gemini_llm(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0
) -> Optional[ChatGoogleGenerativeAI]:
    """Instantiates a Google Gemini chat model."""
    key = api_key or settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY or "dummy-gemini-key"
    model_name = model or settings.GEMINI_MODEL or "gemini-3.5-flash"

    if not model_name.startswith("models/") and not model_name.startswith("gemini-"):
        model_name = "gemini-3.5-flash"

    try:
        return ChatGoogleGenerativeAI(
            model=model_name,
            google_api_key=key,
            temperature=temperature,
        )
    except Exception as e:
        logger.error(f"Failed to instantiate Gemini LLM ({model_name}): {e}")
        return None


def get_openai_llm(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    temperature: float = 0.0
) -> Optional[ChatOpenAI]:
    """Instantiates an OpenAI chat model."""
    key = api_key or settings.OPENAI_API_KEY or "dummy-openai-key"
    model_name = model or settings.OPENAI_MODEL or "gpt-4o-mini"
    try:
        return ChatOpenAI(
            model=model_name,
            api_key=key,
            temperature=temperature,
        )
    except Exception as e:
        logger.error(f"Failed to instantiate OpenAI LLM ({model_name}): {e}")
        return None


def get_llm_by_provider(provider: str, temperature: float = 0.0) -> Optional[BaseChatModel]:
    """Returns an LLM instance corresponding to the provider name."""
    provider_clean = provider.strip().lower()
    if provider_clean in ["gemini", "google", "gemani"]:
        return get_gemini_llm(temperature=temperature)
    elif provider_clean in ["openai", "gpt"]:
        return get_openai_llm(temperature=temperature)
    else:
        logger.warning(f"Unknown provider '{provider}'. Defaulting to Gemini.")
        return get_gemini_llm(temperature=temperature) or get_openai_llm(temperature=temperature)


def get_resilient_llm(temperature: float = 0.0) -> BaseChatModel:
    """Creates a resilient LLM with automatic fallback support.

    If primary provider (e.g. Gemini) fails at runtime, LangChain will automatically
    route the request to the fallback provider (e.g. OpenAI), or vice-versa.
    """
    primary_provider = (settings.PRIMARY_PROVIDER or "gemini").strip().lower()
    fallback_provider = (settings.FALLBACK_PROVIDER or "openai").strip().lower()

    # Determine primary model
    primary_llm = get_llm_by_provider(primary_provider, temperature=temperature)
    
    # Determine fallback models
    fallback_llms: List[BaseChatModel] = []
    if fallback_provider != primary_provider:
        fb_llm = get_llm_by_provider(fallback_provider, temperature=temperature)
        if fb_llm:
            fallback_llms.append(fb_llm)

    # Ensure we always have at least one usable model
    if primary_llm is None:
        if fallback_llms:
            primary_llm = fallback_llms.pop(0)
        else:
            primary_llm = ChatGoogleGenerativeAI(
                model="gemini-3.5-flash",
                google_api_key=settings.GEMINI_API_KEY or settings.GOOGLE_API_KEY or "dummy-gemini-key",
                temperature=temperature
            )

    if fallback_llms:
        logger.info(
            f"Configured resilient LLM: Primary={primary_provider}, Fallback={fallback_provider}"
        )
        return primary_llm.with_fallbacks(fallback_llms)

    return primary_llm
