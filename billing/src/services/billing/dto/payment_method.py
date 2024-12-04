from uuid import UUID

from services.billing.dto.base import Base
from services.billing.dto.types import PaymentMethodType


class PaymentMethod(Base):
    id: UUID
    type: PaymentMethodType
    saved: bool
