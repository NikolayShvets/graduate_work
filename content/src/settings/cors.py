from settings.base import Settings


class CorsSettings(Settings):
    ORIGINS: str


settings = CorsSettings()
