from datetime import datetime
from uuid import UUID

from services.yookassa.dto.amount import Amount
from services.yookassa.dto.base import Base
from services.yookassa.dto.payment_method import PaymentMethod
from services.yookassa.dto.recipient import Recipient
from services.yookassa.dto.types import PaymentStatus


class Payment(Base):
    id: UUID
    status: PaymentStatus
    amount: Amount
    recipient: Recipient
    payment_method: PaymentMethod | None = None
    description: str
    created_at: datetime
    test: bool
    paid: bool
    refundable: bool
