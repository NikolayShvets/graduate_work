from pydantic import HttpUrl, SecretStr

from settings.base import Settings


class YooKassaSettings(Settings):
    ACCOUNT_ID: str
    KASSA_SECRET_KEY: SecretStr
    CONFIRMATION_RETURN_URL: HttpUrl


settings = YooKassaSettings()
