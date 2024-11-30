from settings.base import Settings


class JwtSettings(Settings):
    AUTH_API_URL: str
    JWT_ALGORITHM: str
    SECRET_KEY: str
    AUDIENCE: str = "fastapi"


settings = JwtSettings()
