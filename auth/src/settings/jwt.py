from src.settings.base import Settings


class JWTSettings(Settings):
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_LIFETIME_SECONDS: int = 60 * 15  # 15 minutes
    REFRESH_TOKEN_LIFETIME_SECONDS: int = 60 * 60 * 24 * 14  # 14 days


settings = JWTSettings()
