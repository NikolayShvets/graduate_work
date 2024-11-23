from pydantic import EmailStr

from schemas.base import Base


class Email(Base):
    recipient: EmailStr
    subject: str
    body: str
