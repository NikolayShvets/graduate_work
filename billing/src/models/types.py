from enum import StrEnum


class Currency(StrEnum):
    RUB = "RUB"
    USD = "USD"
    EUR = "EUR"


class AutoPaymentPeriod(StrEnum):
    MONTHLY = "MONTHLY"
    YEARLY = "YEARLY"


class TransactionStatus(StrEnum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELED = "CANCELED"


class TransactionType(StrEnum):
    PAYMENT = "PAYMENT"
    REFUND = "REFUND"
