from app.settings.base import Settings


class LoggingSettings(Settings):
    LOG_FILE_PATH: str
    FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"


settings = LoggingSettings()
