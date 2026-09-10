from langchain_core.tools import tool
from app.config.settings import settings
from app.agents.sql_agents import create_medical_sql_agent
from app.utils.logger import logger

sql_agent = None


def _get_agent():
    global sql_agent
    if sql_agent is None:
        sql_agent = create_medical_sql_agent(settings.CANCER_DB_PATH)
    return sql_agent


@tool
def CancerDBTool(query: str) -> str:
    """Use this tool to query the Cancer Prediction Database.
    Contains records of patient demographics, BMI, smoking status, genetic risk,
    physical activity, alcohol intake, history of cancer, and diagnosis.
    Input should be a clear natural language question about cancer patient statistics or records."""
    try:
        agent = _get_agent()
        if agent is None:
            logger.warning("Cancer SQL agent unavailable, returning fallback notice.")
            return "Cancer database is currently unreachable. Please use general oncology clinical guidelines."

        result = agent.invoke({"input": query})
        output = result.get("output", "").strip()
        return output if output else "No matching cancer patient records found."
    except Exception as e:
        logger.error(f"CancerDBTool execution failed: {e}", exc_info=True)
        return "Unable to retrieve cancer database statistics at this moment. Proceeding with clinical knowledge."