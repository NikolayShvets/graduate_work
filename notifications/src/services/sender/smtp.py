from email.mime.text import MIMEText
from email.utils import formataddr

from aiosmtplib import SMTP, SMTPConnectError, SMTPServerDisconnected, SMTPTimeoutError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from logger import logger
from schemas.message import Message
from settings.smtp import settings as smtp_settings


class EmailSender:
    def __init__(self, conn: SMTP) -> None:
        self._conn = conn

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=10),
        retry=retry_if_exception_type(
            (SMTPServerDisconnected, SMTPConnectError, SMTPTimeoutError)
        ),
        retry_error_callback=lambda retry_state: logger.error(
            f"Unable to send email to {retry_state.args[1].recipients}. "
            f"Attempt {retry_state.attempt_number} failed. "
            f"Error: {retry_state.outcome.exception()}"
        ),
    )
    async def send(self, message: Message) -> None:
        await self._conn.sendmail(
            smtp_settings.SMTP_USER,
            [recipient.email for recipient in message.recipients],
            self._prepare_message(message),
        )

    def _prepare_message(self, message: Message) -> str:
        prepared = MIMEText(message.body, message.mime_type, "utf-8")
        prepared["Subject"] = message.subject
        prepared["From"] = formataddr((None, smtp_settings.SMTP_USER))
        prepared["To"] = ", ".join(
            [recipient.email for recipient in message.recipients]
        )
        return prepared.as_string()
