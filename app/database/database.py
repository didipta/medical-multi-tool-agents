import sqlite3
from pathlib import Path
from langchain_community.utilities import SQLDatabase
from app.utils.logger import logger

def get_db_connection(db_path: Path) -> sqlite3.Connection:
    """Creates and returns a raw sqlite3 connection."""
    try:
        conn = sqlite3.connect(str(db_path))
        return conn
    except Exception as e:
        logger.error(f"Error connecting to database {db_path}: {e}")
        raise

def get_sql_database(db_path: Path) -> SQLDatabase:
    """Wraps SQLite in LangChain's SQLDatabase utility."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database file not found at: {db_path}")
    return SQLDatabase.from_uri(f"sqlite:///{db_path}")