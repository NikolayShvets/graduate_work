from datetime import datetime
from uuid import UUID

from services.billing.dto.amount import Amount
from services.billing.dto.base import Base
from services.billing.dto.payment_method import PaymentMethod
from services.billing.dto.recipient import Recipient
from services.billing.dto.types import PaymentStatus


class Payment(Base):
    id: UUID
    status: PaymentStatus
    amount: Amount
    recipient: Recipient
    payment_method: PaymentMethod
    created_at: datetime
    test: bool
    paid: bool
    refundable: bool
