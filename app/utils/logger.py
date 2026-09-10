import logging
from app.config.settings import settings

settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = settings.LOGS_DIR / "app.log"

logger = logging.getLogger("medical_agent")
logger.setLevel(settings.LOG_LEVEL)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)