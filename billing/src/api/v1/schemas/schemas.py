from pydantic import Field

from src.api.v1.schemas.base import Base


class NewPayment(Base):
    amount: float = Field(description="Стоимость", examples=[100.00, 500.00])
    currency: str = Field(description="Валюта", examples=["RUB"])
    description: str | None = Field(description="Описание", examples=["Оплата подписки"])


class AutoPayment(NewPayment):
    payment_method_id: str = Field(description="ID первого платежа", examples=["255350c9-000f-5000-a000-1f211b3ea0a7"])


class OutputNewPayment(Base):
    id: str = Field(description="ID платежа", examples=["255350c9-000f-5000-a000-1f211b3ea0a7"])
    status: str = Field(description="Статус", examples=["pending"])
    confirmation_url: str = Field(description="Url для ввода данных карты", examples=[
        "https://yoomoney.ru/checkout/payments/v2/contract?orderId=2ed2dbcb-000f-5000-8000-13bfc21ebf22"])
    payment_method_id: str | None = Field(description="Id главного платежа",
                                          examples=["255350c9-000f-5000-a000-1f211b3ea0a7"])
    payment_method_saved: bool | None = Field(description="Состояние платежа", examples=[True, False])


class InputRefund(Base):
    payment_id: str = Field(description="ID платежа", examples=["255350c9-000f-5000-a000-1f211b3ea0a7"])
    amount: float = Field(description="Стоимость", examples=[100.00, 500.00])
    currency: str = Field(description="Валюта", examples=["RUB"])
