from enum import StrEnum

from schemas.base import Base
from schemas.user import User


class MimeType(StrEnum):
    HTML = "html"
    TEXT = "text"


class Message(Base):
    recipients: list[User]
    subject: str
    body: str
    mime_type: MimeType = MimeType.TEXT
