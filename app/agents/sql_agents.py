from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from app.config.settings import settings
from app.database.database import get_sql_database

def create_medical_sql_agent(db_path: Path):
    """Initializes a specialized SQL sub-agent for a given database."""
    db = get_sql_database(db_path)
    llm = ChatOpenAI(
        model=settings.OPENAI_MODEL,
        temperature=0,
        api_key=settings.OPENAI_API_KEY
    )
    return create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        verbose=False
    )