"""Interactive CLI for the Medical AI Multi-Tool Agent System.

Includes Gemini and OpenAI model support, automatic fallback mechanisms,
and guaranteed fallback answers without error modals or stack traces.
"""

from app.agents.medical_agent import initialize_medical_agent
from app.utils.fallback_answers import get_fallback_medical_answer
from app.config.settings import settings
from app.utils.logger import logger


def start_interactive_session():
    """Starts the interactive medical assistant session."""
    logger.info("Initializing Medical AI Multi-Tool Agent system...")

    primary_name = settings.PRIMARY_PROVIDER.upper()
    fallback_name = settings.FALLBACK_PROVIDER.upper()

    print("\n" + "=" * 65)
    print("  🏥 Medical AI Multi-Tool Agent System")
    print(f"  🤖 Primary Provider: {primary_name} | Fallback Provider: {fallback_name}")
    print("  Type 'exit' or 'quit' to end the session.")
    print("=" * 65 + "\n")

    try:
        agent_executor = initialize_medical_agent()
    except Exception as init_err:
        logger.error(f"Failed to initialize agent executor: {init_err}", exc_info=True)
        agent_executor = None

    while True:
        try:
            user_query = input("\nUser: ").strip()
            if not user_query:
                continue
            if user_query.lower() in ["exit", "quit"]:
                print("\nExiting session. Take care and stay healthy!")
                break

            if agent_executor is None:
                # Direct fallback when agent failed initialization
                fallback_ans = get_fallback_medical_answer(user_query)
                print(f"\nAgent:\n{fallback_ans}")
                continue

            response = agent_executor.invoke({"input": user_query})
            output = response.get("output", "").strip()

            if not output:
                output = get_fallback_medical_answer(user_query)

            print(f"\nAgent:\n{output}")

        except KeyboardInterrupt:
            print("\n\nSession stopped by user. Goodbye!")
            break
        except Exception as e:
            logger.error(f"Unexpected error while handling query '{user_query}': {e}", exc_info=True)
            fallback_ans = get_fallback_medical_answer(user_query, error=e)
            print(f"\nAgent:\n{fallback_ans}")