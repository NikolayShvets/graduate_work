import logger
import os

from settings.logger import settings as logging_settings

os.makedirs(os.path.dirname(logging_settings.LOG_FILE_PATH), exist_ok=True)

logger.basicConfig(
    level=logger.INFO,
    format=logging_settings.LOG_FORMAT,
    handlers=[
        logger.FileHandler(logging_settings.LOG_FILE_PATH),
        logger.StreamHandler(),
    ],
)

logger = logger.getLogger(logging_settings.LOG_NAME)
