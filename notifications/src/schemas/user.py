from pydantic import EmailStr

from schemas.base import Base


class User(Base):
    email: EmailStr
    name: str
    surname: str | None = None
    patronymic: str | None = None
