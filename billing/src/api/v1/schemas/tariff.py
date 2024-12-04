from datetime import datetime
from decimal import Decimal
from uuid import UUID

from api.v1.schemas.base import Base
from models.types import AutoPaymentPeriod, Currency


class TariffBaseSchema(Base):
    name: str
    description: str
    plan_id: UUID
    currency: Currency
    price: Decimal
    auto_payment_period: AutoPaymentPeriod


class TariffCreateSchema(TariffBaseSchema):
    pass


class TariffUpdateSchema(TariffBaseSchema):
    pass


class TariffRetrieveSchema(TariffBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime
