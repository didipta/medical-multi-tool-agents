import sys
from pathlib import Path
import pandas as pd

# Add root folder to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.append(str(root_dir))

from app.config.settings import settings
from app.database.database import get_db_connection
from app.utils.logger import logger

DATASETS = [
    {
        "csv": settings.DATA_DIR / "heart_disease.csv",
        "db": settings.HEART_DB_PATH,
        "table": "heart_patients"
    },
    {
        "csv": settings.DATA_DIR / "cancer.csv",
        "db": settings.CANCER_DB_PATH,
        "table": "cancer_patients"
    },
    {
        "csv": settings.DATA_DIR / "diabetes.csv",
        "db": settings.DIABETES_DB_PATH,
        "table": "diabetes_patients"
    }
]

def build_databases():
    settings.DATABASES_DIR.mkdir(parents=True, exist_ok=True)

    for item in DATASETS:
        csv_path = item["csv"]
        db_path = item["db"]
        table_name = item["table"]

        if not csv_path.exists():
            logger.warning(f"CSV file not found at {csv_path}. Skipping.")
            continue

        try:
            df = pd.read_csv(csv_path)
            # Normalize column names: strip spaces and convert to lower
            df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

            conn = get_db_connection(db_path)
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            conn.close()
            logger.info(f"Loaded {len(df)} rows into {db_path.name} -> table: {table_name}")
        except Exception as e:
            logger.error(f"Failed to process {csv_path.name}: {e}")

if __name__ == "__main__":
    build_databases()