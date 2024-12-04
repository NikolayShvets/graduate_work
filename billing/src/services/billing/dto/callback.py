from services.billing.dto.base import Base
from services.billing.dto.payment import Payment
from services.billing.dto.types import EventType


class Callback(Base):
    type: str
    event: EventType
    object: Payment
