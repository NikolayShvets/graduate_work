from app.settings.base import Settings


class JWTSettings(Settings):
    ALGORITHM: str
    ACCESS_TOKEN_LIFETIME_SECONDS: int
    REFRESH_TOKEN_LIFETIME_SECONDS: int


settings = JWTSettings()
