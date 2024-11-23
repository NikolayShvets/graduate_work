from uuid import UUID

from schemas.base import Base
from schemas.user import User


class Notification(Base):
    id: UUID
    users: list[User]
    template: str
