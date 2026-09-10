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
        result = agent.invoke({"input": query})
        return result.get("output", "No response generated.")
    except Exception as e:
        logger.error(f"DiabetesDBTool execution failed: {e}")
        return f"Error querying Diabetes Database: {str(e)}"