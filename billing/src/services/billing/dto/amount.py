from decimal import Decimal

from services.billing.dto.base import Base
from services.billing.dto.types import Currency


class Amount(Base):
    value: Decimal
    currency: Currency
