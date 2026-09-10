from app.agents.medical_agent import initialize_medical_agent
from app.utils.logger import logger

def start_interactive_session():
    logger.info("Initializing Medical AI Agent system...")
    agent_executor = initialize_medical_agent()
    print("\n" + "=" * 60)
    print(" Medical AI Multi-Tool Agent Ready (Type 'exit' to quit)")
    print("=" * 60 + "\n")

    while True:
        try:
            user_query = input("\nUser: ").strip()
            if not user_query:
                continue
            if user_query.lower() in ["exit", "quit"]:
                print("Exiting session. Goodbye!")
                break

            response = agent_executor.invoke({"input": user_query})
            print(f"\nAgent:\n{response['output']}")
        except KeyboardInterrupt:
            print("\nSession stopped.")
            break
        except Exception as e:
            logger.error(f"Error handling query: {e}")
            print(f"\nAn error occurred: {e}")