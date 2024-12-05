from typing import Literal

from services.yookassa.dto.base import Base
from services.yookassa.dto.payment import Payment
from services.yookassa.dto.types import EventType


class Callback(Base):
    type: Literal["notification"]
    event: EventType
    object: Payment
