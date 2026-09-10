from pathlib import Path
from typing import Any
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = BASE_DIR / ".env"


class Settings(BaseSettings):
   
    OPENAI_API_KEY: str = ""
    TAVILY_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LOG_LEVEL: str = "INFO"


    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    DATABASES_DIR: Path = BASE_DIR / "databases"
    LOGS_DIR: Path = BASE_DIR / "logs"


    HEART_DB_PATH: Path = DATABASES_DIR / "heart_disease.db"
    CANCER_DB_PATH: Path = DATABASES_DIR / "cancer.db"
    DIABETES_DB_PATH: Path = DATABASES_DIR / "diabetes.db"

  
    @property
    def DATABASE_MAP(self) -> dict[str, dict[str, Any]]:
        return {
            "heart_disease": {
                "csv": self.DATA_DIR / "heart_disease.csv",
                "db": self.HEART_DB_PATH,
                "table": "heart_patients",
                "display_name": "Heart Disease Database",
            },
            "cancer": {
                "csv": self.DATA_DIR / "cancer.csv",
                "db": self.CANCER_DB_PATH,
                "table": "cancer_patients",
                "display_name": "Cancer Prediction Database",
            },
            "diabetes": {
                "csv": self.DATA_DIR / "diabetes.csv",
                "db": self.DIABETES_DB_PATH,
                "table": "diabetes_patients",
                "display_name": "Diabetes Database",
            },
        }

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()