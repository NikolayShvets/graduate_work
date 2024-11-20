from src.settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "billing-api"
    OPENAPI_URL: str = "/api/billing/openapi.json"
    DOCS_URL: str = "/api/billing/docs"
    REDOC_URL: str = "/api/billing/redoc"
    SECRET_KEY: str


settings = ApiSettings()
