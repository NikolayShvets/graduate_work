from pydantic import SecretStr

from settings.base import Settings


class SMTPSettings(Settings):
    SMTP_HOST: str = "localhost"
    SMTP_PORT: int = 25
    SMTP_USER: str = "test@gmail.com"
    SMTP_PASSWORD: SecretStr


settings = SMTPSettings()
