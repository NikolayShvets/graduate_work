from decimal import Decimal

from services.yookassa.dto.base import Base
from services.yookassa.dto.types import Currency


class Amount(Base):
    value: Decimal
    currency: Currency
