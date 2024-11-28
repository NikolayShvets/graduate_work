from settings.base import Settings


class LoggingSettings(Settings):
    LOG_FILE_PATH: str
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    LOG_NAME: str


settings = LoggingSettings()
