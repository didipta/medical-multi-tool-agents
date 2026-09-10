from pathlib import Path
from langchain_community.agent_toolkits import create_sql_agent
from app.database.database import get_sql_database
from app.utils.llm_factory import get_resilient_llm
from app.utils.logger import logger


def create_medical_sql_agent(db_path: Path):
    """Initializes a specialized SQL sub-agent for a given database using resilient LLMs."""
    try:
        db = get_sql_database(db_path)
        llm = get_resilient_llm(temperature=0)
        return create_sql_agent(
            llm=llm,
            db=db,
            agent_type="tool-calling",
            verbose=False,
            handle_parsing_errors=True
        )
    except Exception as e:
        logger.error(f"Error creating SQL agent for {db_path}: {e}", exc_info=True)
        return None