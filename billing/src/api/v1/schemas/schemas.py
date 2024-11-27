from enum import StrEnum, auto
from uuid import UUID

from pydantic import Field

from api.v1.schemas.base import Base


class StatusEnum(StrEnum):
    pending = auto()
    closed = auto()


class CurrencyEnum(StrEnum):
    RUB = auto()
    ENG = auto()


class NewPaymentScheme(Base):
    amount: float = Field(description="Стоимость", examples=[100.00, 500.00])
    currency: str = Field(description="Валюта", examples=["RUB"])
    description: str | None = Field(
        description="Описание", examples=["Оплата подписки"]
    )


class AutoPaymentScheme(NewPaymentScheme):
    payment_method_id: UUID = Field(
        description="ID первого платежа",
        examples=["255350c9-000f-5000-a000-1f211b3ea0a7"],
    )


class OutputNewPaymentScheme(Base):
    id: str = Field(
        description="ID платежа", examples=["255350c9-000f-5000-a000-1f211b3ea0a7"]
    )
    status: StatusEnum = Field(description="Статус", examples=[StatusEnum.pending])
    confirmation_url: str = Field(
        description="Url для ввода данных карты",
        examples=[
            "https://yoomoney.ru/checkout/payments/v2/contract?orderId=2ed2dbcb-000f-5000"
        ],
    )
    payment_method_id: UUID | None = Field(
        description="Id главного платежа",
        examples=["255350c9-000f-5000-a000-1f211b3ea0a7"],
    )
    payment_method_saved: bool | None = Field(
        description="Состояние платежа", examples=[True, False]
    )


class InputRefundScheme(Base):
    payment_id: UUID = Field(
        description="ID платежа", examples=["255350c9-000f-5000-a000-1f211b3ea0a7"]
    )
    amount: float = Field(description="Стоимость", examples=[100.00, 500.00])
    currency: CurrencyEnum = Field(
        description="Валюта", examples=[CurrencyEnum.RUB, CurrencyEnum.ENG]
    )
