from pydantic import SecretStr

from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "auth-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    SECRET_KEY: SecretStr
    ORIGINS: list[str] = ["http://127.0.0.1:8002", "http://127.0.0.1:8003"]


settings = ApiSettings()
