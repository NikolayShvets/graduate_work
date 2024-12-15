from settings.base import Settings


class ApiSettings(Settings):
    TITLE: str = "content-api"
    OPENAPI_URL: str = "/api/openapi.json"
    DOCS_URL: str = "/api/docs"
    REDOC_URL: str = "/api/redoc"
    EXTERNAL_LOGIN_URL: str = "http://127.0.0.1:8000/auth/api/v1/jwt/login"
    AUTH_API_URL: str = "http://auth:8001"
    BILLING_API_URL: str = "http://billing:8002"


settings = ApiSettings()
