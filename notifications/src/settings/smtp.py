from pydantic import SecretStr

from settings.base import Settings


class SMTPSettings(Settings):
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: SecretStr


settings = SMTPSettings()
