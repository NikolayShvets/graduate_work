from enum import StrEnum, auto
from uuid import UUID

from notifications.schemas.base import Base
from notifications.schemas.user import User


class EventType(StrEnum):
    USER_REGISTERED = auto()
    USER_LOGGED_IN = auto()


class Notification(Base):
    id: UUID
    event_type: EventType
    user: User
