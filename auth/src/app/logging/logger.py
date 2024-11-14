import logging
import os

from app.settings.logging import settings as logging_settings

os.makedirs(os.path.dirname(logging_settings.LOG_FILE_PATH), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format=logging_settings.FORMAT,
    handlers=[
        logging.FileHandler(logging_settings.LOG_FILE_PATH),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger("auth")
