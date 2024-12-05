from settings.base import Settings


class ApiSettings(Settings):
    ROOT_PATH: str = "/billing"
    TITLE: str = "billing-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    EXTERNAL_LOGIN_URL: str = "http://127.0.0.1:8000/auth/api/v1/jwt/login"
    AUTH_API_URL: str = "http://auth:8001"


settings = ApiSettings()
