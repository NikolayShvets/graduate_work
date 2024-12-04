from datetime import datetime
from enum import StrEnum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field, HttpUrl, field_validator


class InitiatorsPaymentCancellationEnum(StrEnum):
    MERCHANT = "merchant"
    YOOMONEY = "yoo_money"
    PAYMENT_NETWORK = "payment_network"


class ReasonsPaymentCancellationEnum(StrEnum):
    THREE_D_SECURE_FAILED = "3d_secure_failed"
    CALL_ISSUER = "call_issuer"
    CANCELED_BY_MERCHANT = "canceled_by_merchant"
    CARD_EXPIRED = "card_expired"
    COUNTRY_FORBIDDEN = "country_forbidden"
    DEAL_EXPIRED = "deal_expired"
    EXPIRED_ON_CAPTURE = "expired_on_capture"
    EXPIRED_ON_CONFIRMATION = "expired_on_confirmation"
    FRAUD_SUSPECTED = "fraud_suspected"
    GENERAL_DECLINE = "general_decline"
    IDENTIFICATION_REQUIRED = "identification_required"
    INSUFFICIENT_FUNDS = "insufficient_funds"
    INTERNAL_TIMEOUT = "internal_timeout"
    INVALID_CARD_NUMBER = "invalid_card_number"
    INVALID_CSC = "invalid_csc"
    ISSUER_UNAVAILABLE = "issuer_unavailable"
    PAYMENT_METHOD_LIMIT_EXCEEDED = "payment_method_limit_exceeded"
    PAYMENT_METHOD_RESTRICTED = "payment_method_restricted"
    PERMISSION_REVOKED = "permission_revoked"
    UNSUPPORTED_MOBILE_OPERATOR = "unsupported_mobile_operator"


class CurrencyEnum(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class StatusEnum(StrEnum):
    PENDING = "pending"
    SUCCESS = "succeeded"
    CANCELED = "canceled"
    WAITING_FOR_CAPTURE = "waiting_for_capture"


class AmountScheme(BaseModel):
    currency: CurrencyEnum = Field(description="Трехбуквенный код валюты.")
    value: str = Field(description="Сумма в выбранной валюте.")


class Confirmation(BaseModel):
    confirmation_url: HttpUrl | None = Field(
        default=None,
        description="URL-адрес, на который будет перенаправлен пользователь "
        "для подтверждения платежа.",
    )
    return_url: HttpUrl | None = Field(
        default=None,
        description="URL-адрес, по которому пользователь вернется после "
        "подтверждения/отмены платежа на веб-странице.",
    )
    enforce: bool | None = Field(
        default=None,
        description="Запрос на проведение платежа с аутентификацией по 3-D Secure.",
    )
    type: str | None = Field(default=None, description="Значение: перенаправление.")


class RecipientScheme(BaseModel):
    account_id: int = Field(description="ID магазина в YooMoney.")
    gateway_id: int = Field(description="ID субаккаунта.")

    @classmethod
    @field_validator("account_id", "gateway_id")
    def validate_uuid(cls, value):
        if isinstance(value, str):
            return int(value)
        elif isinstance(value, int):
            return value
        raise TypeError("Тип данных должен быть int.")


class PaymentMethodScheme(BaseModel):
    id: UUID
    saved: bool = Field(
        description="Метод сохранения платежа для возможности автоматической полаты."
    )
    title: str = Field(description="Название способа оплаты.")
    type: str = Field(description="Код способа оплаты.")

    @classmethod
    @field_validator("id")
    def validate_uuid(cls, value: str) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        elif isinstance(value, UUID):
            return value
        raise TypeError("Тип данных должен быть UUID.")


class CancellationDetailsScheme(BaseModel):
    party: InitiatorsPaymentCancellationEnum = Field(
        description="Инициаторы отмены платежа.",
        examples=[*InitiatorsPaymentCancellationEnum],
    )
    reason: ReasonsPaymentCancellationEnum = Field(
        description="Причины отмены платежа.",
        examples=[*ReasonsPaymentCancellationEnum],
    )


class OutputPaymentScheme(BaseModel):
    id: UUID = Field(
        description="ID платежа в YooMoney.",
        examples=["2edf862d-000f-5000-a000-15598219bb7c"],
    )
    amount: AmountScheme = Field(
        description="Сумма платежа.",
    )
    income_amount: AmountScheme | None = Field(
        default=None,
        description="Сумма платежа, которую должен получить магазин.",
    )
    refunded_amount: AmountScheme | None = Field(
        default=None, description="Сумма, возвращенная пользователю."
    )
    confirmation: Confirmation | None = Field(
        default=None, description="Выбранный сценарий подтверждения платежа."
    )
    description: str = Field(description="Описание транзакции.")
    metadata: Any = Field(
        description="Любые дополнительные данные, которые могут потребоваться вам "
        "для обработки платежей."
    )
    cancellation_details: CancellationDetailsScheme | None = Field(
        default=None,
        description="Комментарий к статусу «Отменено»: кто и почему отменил платеж.",
    )
    payment_method: PaymentMethodScheme | None = Field(
        default=None, description="Способ оплаты."
    )
    status: StatusEnum = Field(description="Статус платежа.", examples=[*StatusEnum])
    recipient: RecipientScheme = Field(description="Получатель платежа.")
    refundable: bool = Field(
        description="Наличие возможности осуществить возврат средств через API."
    )
    paid: bool = Field(description="Атрибут оплаченного заказа.")
    test: bool = Field(description="Атрибут тестовой транзакции.")
    captured_at: datetime | None = Field(
        default=None, description="Время получения платежа."
    )
    expires_at: datetime | None = Field(
        default=None,
        description="Период, в течение которого можно бесплатно отменить "
        "или получить платеж.",
    )
    created_at: datetime = Field(description="Время создания платежа.")

    @classmethod
    @field_validator("created_at", "expires_at", "captured_at")
    def validate_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value[:-1])
        return value

    @classmethod
    @field_validator("id")
    def validate_uuid(cls, value: str) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        elif isinstance(value, UUID):
            return value
        raise TypeError("Тип данных должен быть UUID.")


class OutputRefundScheme(BaseModel):
    id: UUID = Field(
        description="ID возврата в YooMoney.",
        examples=["2edf862d-000f-5000-a000-15598219bb7c"],
    )
    amount: AmountScheme = Field(
        description="Сумма, возвращенная пользователю.",
    )
    payment_id: str = Field(description="Идентификатор платежа в ЮKassa.")
    status: StatusEnum = Field(
        description="Статус возврата платежа.", examples=[*StatusEnum]
    )
    description: str | None = Field(
        default=None, description="Основание для возврата денег пользователю."
    )
    cancellation_details: CancellationDetailsScheme | None = Field(
        default=None,
        description="Комментарий к статусу «Отменено»: кто и почему отменил платеж.",
    )
    created_at: str = Field(description="Время создания возврата.")

    @classmethod
    @field_validator("id")
    def validate_uuid(cls, value: str) -> UUID:
        if isinstance(value, str):
            return UUID(value)
        elif isinstance(value, UUID):
            return value
        raise TypeError("Тип данных должен быть UUID.")

    @classmethod
    @field_validator("created_at")
    def validate_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value[:-1])
        return value
