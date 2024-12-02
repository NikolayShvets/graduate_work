from pydantic import SecretStr

from settings.base import Settings


class YooKassaSettings(Settings):
    ACCOUNT_ID: str
    KASSA_SECRET_KEY: SecretStr


settings = YooKassaSettings()
