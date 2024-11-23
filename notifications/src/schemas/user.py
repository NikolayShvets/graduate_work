from schemas.base import Base


class User(Base):
    email: str
    name: str
    surname: str | None = None
    patronymic: str | None = None
