from datetime import datetime
from uuid import UUID

from services.yookassa.dto.amount import Amount
from services.yookassa.dto.base import Base
from services.yookassa.dto.types import RefundStatus


class Refund(Base):
    id: UUID
    payment_id: UUID
    status: RefundStatus
    amount: Amount
    created_at: datetime
