from settings.base import Settings


class LoggerSettings(Settings):
    LOG_FILE_PATH: str = "/var/log/.log"
    LOG_FORMAT: str = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    LOG_NAME: str = "auth"


settings = LoggerSettings()
