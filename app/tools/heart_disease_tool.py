from langchain_core.tools import tool
from app.config.settings import settings
from app.agents.sql_agents import create_medical_sql_agent
from app.utils.logger import logger

sql_agent = None

def _get_agent():
    global sql_agent
    if sql_agent is None:
        sql_agent = create_medical_sql_agent(settings.HEART_DB_PATH)
    return sql_agent

@tool
def HeartDiseaseDBTool(query: str) -> str:
    """Use this tool to query the Heart Disease Database.
    Contains patient information: age, sex, chest pain type (cp), resting blood pressure (trestbps),
    cholesterol (chol), fasting blood sugar (fbs), restecg, max heart rate (thalach),
    exercise angina (exang), oldpeak, slope, ca, thal, and target heart disease status.
    Input should be a clear natural language question about heart disease patient data."""
    try:
        agent = _get_agent()
        result = agent.invoke({"input": query})
        return result.get("output", "No response generated.")
    except Exception as e:
        logger.error(f"HeartDiseaseDBTool execution failed: {e}")
        return f"Error querying Heart Disease Database: {str(e)}"