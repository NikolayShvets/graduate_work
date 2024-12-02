from enum import StrEnum, auto
from uuid import UUID

from schemas.base import Base
from schemas.user import User


class EventType(StrEnum):
    USER_REGISTERED = auto()
    USER_LOGGED_IN = auto()


class DeliveryMethod(StrEnum):
    EMAIL = auto()
    SMS = auto()


class Notification(Base):
    id: UUID
    event_type: EventType
    user: User
