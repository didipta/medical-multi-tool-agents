from typing import Optional
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

from app.config.settings import settings
from app.utils.logger import logger

_search_tool: Optional[TavilySearchResults] = None


def _get_search_tool() -> Optional[TavilySearchResults]:
    global _search_tool
    if _search_tool is None and settings.TAVILY_API_KEY:
        try:
            _search_tool = TavilySearchResults(
                tavily_api_key=settings.TAVILY_API_KEY,
                max_results=3,
            )
        except Exception as e:
            logger.error(f"Failed to initialize Tavily search: {e}")
            _search_tool = None
    return _search_tool


@tool
def MedicalWebSearchTool(query: str) -> str:
    """
    Use this tool ONLY for general medical knowledge, definitions,
    symptoms, cures, causes, disease overviews, and clinical guidelines.

    Do NOT use this tool for database-specific record lookups
    or numbers from datasets.
    """
    try:
        searcher = _get_search_tool()
        if searcher is None:
            logger.warning("Medical web search tool is not configured or offline.")
            return "Live web search is unavailable. Please rely on standard medical reference knowledge."

        results = searcher.invoke({"query": query})

        if not results:
            return "No verified medical web results found for this query."

        formatted = []
        for r in results:
            content = r.get("content", "").strip()
            source = r.get("url", "").strip()
            if content:
                formatted.append(f"Content: {content}\nSource: {source}")

        return "\n\n".join(formatted) if formatted else "No medical content returned from search."

    except Exception as e:
        logger.error(
            f"MedicalWebSearchTool execution failed: {e}",
            exc_info=True,
        )
        return "Live medical web search encountered a connection issue. Proceeding with standard clinical guidance."