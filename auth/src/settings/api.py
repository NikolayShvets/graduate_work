from pydantic import SecretStr

from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "auth-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    SECRET_KEY: SecretStr
    ORIGINS: list[str]


settings = ApiSettings()
