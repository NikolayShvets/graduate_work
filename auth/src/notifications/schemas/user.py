from pydantic import EmailStr

from notifications.schemas.base import Base


class User(Base):
    email: EmailStr
    name: str | None = None
    surname: str | None = None
    patronymic: str | None = None
