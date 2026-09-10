import logging
from app.config.settings import settings

settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
log_file = settings.LOGS_DIR / "app.log"

logger = logging.getLogger("medical_agent")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Detailed file logging for debugging & tracking
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    # Clean console handler to prevent error modals or distracting tracebacks
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.CRITICAL)
    logger.addHandler(console_handler)