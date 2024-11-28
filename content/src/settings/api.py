from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "content-api"
    OPENAPI_URL: str = "/api/content/openapi.json"
    DOCS_URL: str = "/api/content/docs"
    REDOC_URL: str = "/api/content/redoc"
    SECRET_KEY: str


settings = ApiSettings()
