from langchain_core.tools import tool
from app.config.settings import settings
from app.agents.sql_agents import create_medical_sql_agent
from app.utils.logger import logger

sql_agent = None


def _get_agent():
    global sql_agent
    if sql_agent is None:
        sql_agent = create_medical_sql_agent(settings.DIABETES_DB_PATH)
    return sql_agent


@tool
def DiabetesDBTool(query: str) -> str:
    """Use this tool to query the Diabetes Database.
    Contains parameters: pregnancies, glucose levels, blood pressure, skin thickness,
    insulin, BMI, diabetes pedigree function, age, and diabetes outcome.
    Input should be a clear natural language question about diabetes dataset records or metrics."""
    try:
        agent = _get_agent()
        if agent is None:
            logger.warning("Diabetes SQL agent unavailable, returning fallback notice.")
            return "Diabetes database is currently unreachable. Please use standard metabolic clinical guidelines."

        result = agent.invoke({"input": query})
        output = result.get("output", "").strip()
        return output if output else "No matching diabetes patient records found."
    except Exception as e:
        logger.error(f"DiabetesDBTool execution failed: {e}", exc_info=True)
        return "Unable to retrieve diabetes database records at this time. Proceeding with clinical knowledge."