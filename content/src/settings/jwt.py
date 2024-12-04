from pydantic import SecretStr

from settings.base import Settings


class JWTSettings(Settings):
    ALGORITHM: str = "HS256"
    SECRET_KEY: SecretStr
    AUD: str = "fastapi-users:auth"


settings = JWTSettings()
