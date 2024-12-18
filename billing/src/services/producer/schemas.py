from enum import StrEnum, auto
from uuid import UUID

from pydantic import BaseModel, EmailStr


class EventType(StrEnum):
    SUBSCRIPTION_PAID = auto()
    SUBSCRIPTION_CANCELED = auto()
    SUBSCRIPTION_REFUNDED = auto()


class User(BaseModel):
    email: EmailStr
    name: str


class Notification(BaseModel):
    id: UUID
    event_type: EventType
    user: User
