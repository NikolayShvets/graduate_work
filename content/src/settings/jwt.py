from src.settings.base import Settings


class JwtSettings(Settings):
    AUTH_API_URL: str
    JWT_ALGORITHM: str
    AUDIENCE: str = "fastapi"
    SECRET_KEY: str


settings = JwtSettings()
