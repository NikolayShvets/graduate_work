import logging

from fastapi import HTTPException
from yookassa import Payment, Refund
from yookassa.client import NotFoundError
from yookassa.domain.exceptions import BadRequestError

from api.v1.schemas.schemas import (
    AutoPaymentScheme,
    InputRefundScheme,
    NewPaymentScheme,
)

from services.schemas.schemas import OutputPaymentScheme, OutputRefundScheme


class YooKassaBilling:
    """Класс биллинга YooKassa"""

    def __init__(self):
        self.log = logging.getLogger("main")

    def create_payment(self, data: NewPaymentScheme) -> OutputPaymentScheme:
        """
        Функция создает новый платеж.
        """
        try:
            payment = Payment.create(
                {
                    "amount": {
                        "value": data.amount,
                        "currency": data.currency.RUB,
                    },
                    "confirmation": {
                        "type": "redirect",
                        "return_url": "https://www.example.com/return_url",
                    },
                    "capture": True,
                    "description": data.description,
                    "save_payment_method": True,
                }
            )
        except Exception as e:
            self.log.error(e)
            raise HTTPException(status_code=404, detail="Item not created") from None

        return OutputPaymentScheme(**dict(payment))

    def create_auto_payment(self, data: AutoPaymentScheme) -> OutputPaymentScheme:
        """
        Создает новый платеж из основного платежа. Данные карты не требуются.
        """
        try:
            payment = Payment.create(
                {
                    "amount": {
                        "value": data.amount,
                        "currency": data.currency,
                    },
                    "capture": True,
                    "payment_method_id": data.payment_method_id,
                    "description": data.description,
                }
            )
        except Exception as e:
            self.log.error(e)
            raise HTTPException(status_code=404, detail="Item not created") from None

        return OutputPaymentScheme(**dict(payment))

    def get_payment(self, payment_id: str) -> OutputPaymentScheme:
        """
        Получает данные о платеже
        """
        try:
            payment = Payment.find_one(payment_id)
        except NotFoundError:
            self.log.error("Item not found")
            raise HTTPException(status_code=404, detail="Item not found") from None

        return OutputPaymentScheme(**dict(payment))

    def create_refund(self, data: InputRefundScheme) -> OutputRefundScheme:
        """
        Создает возврат средств.
        """
        try:
            refund = Refund.create(
                {
                    "amount": {
                        "value": data.amount,
                        "currency": data.currency,
                    },
                    "payment_id": str(data.payment_id),
                }
            )
        except BadRequestError as err:
            self.log.error("Не удалось создать возврат")
            raise HTTPException(
                status_code=404, detail="Failed to create refund"
            ) from err

        return OutputRefundScheme(**dict(refund))
