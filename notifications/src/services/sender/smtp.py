from email.mime.text import MIMEText

from aiosmtplib import SMTP, SMTPConnectError, SMTPServerDisconnected, SMTPTimeoutError
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

from logger import logger
from schemas.email import Email
from settings.smtp import settings as smtp_settings


class EmailSender:
    def __init__(self, conn: SMTP) -> None:
        self._conn = conn

    def get_message(self, email: Email) -> str:
        # TODO: убрать хардкод - метод не должен знать про html
        message = MIMEText(email.body, "html")
        message["Subject"] = email.subject
        message["To"] = email.recipient
        return message

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_random_exponential(min=1, max=10),
        retry=retry_if_exception_type(
            (SMTPServerDisconnected, SMTPConnectError, SMTPTimeoutError)
        ),
        retry_error_callback=lambda retry_state: logger.error(
            f"Unable to send email to {retry_state.args[0].recipient}. "
            f"Attempt {retry_state.attempt_number} failed. "
            f"Error: {retry_state.outcome.exception()}"
        ),
    )
    async def send(self, email: Email) -> None:
        await self._conn.sendmail(
            smtp_settings.SMTP_USER,
            email.recipient,
            self.get_message(email).as_string(),
        )
