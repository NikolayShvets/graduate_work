from uuid import UUID

from services.yookassa.dto.base import Base
from services.yookassa.dto.types import PaymentMethodType


class PaymentMethod(Base):
    id: UUID
    type: PaymentMethodType
    saved: bool
