from pydantic import SecretStr

from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "content-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    SECRET_KEY: SecretStr
    AUTH_API_URL: str = "http://127.0.0.1:8001"


settings = ApiSettings()
