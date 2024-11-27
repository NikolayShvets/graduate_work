import logging
from uuid import UUID

from fastapi import HTTPException
from yookassa import Payment, Refund
from yookassa.client import NotFoundError
from yookassa.domain.exceptions import BadRequestError

from api.v1.schemas.schemas import (
    AutoPaymentScheme,
    InputRefundScheme,
    NewPaymentScheme,
    OutputNewPaymentScheme,
)


class YooKassaBilling:
    """Класс биллинга YooKassa"""

    def __init__(self):
        self.log = logging.getLogger("main")

    def create_payment(self, data: NewPaymentScheme) -> OutputNewPaymentScheme:
        """
        Функция создает новый платеж.
        """
        try:
            payment = Payment.create(
                {
                    "amount": {
                        "value": data.amount,
                        "currency": data.currency,
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

            method_save = (
                payment.payment_method.saved
                if hasattr(payment.payment_method, "saved")
                else None
            )
            method_id = (
                UUID(payment.payment_method.id)
                if hasattr(payment.payment_method, "id")
                else None
            )
            # должна быть функция сохранения payment_method.id в бд для автоплатежей
            return OutputNewPaymentScheme(
                id=UUID(payment.id),
                status=payment.status,
                confirmation_url=payment.confirmation.confirmation_url,
                payment_method_id=method_id,
                payment_method_saved=method_save,
            )

        except Exception as e:
            self.log.error(e)

    def create_auto_payment(self, data: AutoPaymentScheme) -> OutputNewPaymentScheme:
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
            confirmation_url = None
            if hasattr(payment.confirmation, "confirmation_url"):
                confirmation_url = payment.confirmation.confirmation_url

            payment_method_saved = None
            if hasattr(payment.payment_method, "saved"):
                payment_method_saved = payment.payment_method.saved

            payment_method_id = None
            if hasattr(payment.payment_method, "id"):
                payment_method_id = UUID(payment.payment_method.id)
            # должна быть функция сохранения payment_method.id в бд для автоплатежей
            return OutputNewPaymentScheme(
                id=UUID(payment.id),
                status=payment.status,
                confirmation_url=confirmation_url,
                payment_method_id=payment_method_id,
                payment_method_saved=payment_method_saved,
            )
        except Exception as e:
            self.log.error(e)

    def get_payment(self, payment_id: str) -> dict:
        """
        Получает данные о платеже
        """
        try:
            payment = Payment.find_one(payment_id)
        except NotFoundError:
            self.log.error("Item not found")
            raise HTTPException(status_code=404, detail="Item not found") from None

        confirmation_url = None
        if hasattr(payment.confirmation, "confirmation_url"):
            confirmation_url = payment.confirmation.confirmation_url

        payment_method_saved = None
        if hasattr(payment.payment_method, "saved"):
            payment_method_saved = payment.payment_method.saved

        payment_method_id = None
        if hasattr(payment.payment_method, "id"):
            payment_method_id = UUID(payment.payment_method.id)

        cancellation_details_party = None
        if hasattr(payment.cancellation_details, "party"):
            cancellation_details_party = payment.cancellation_details.party

        cancellation_details_reason = None
        if hasattr(payment.cancellation_details, "reason"):
            cancellation_details_reason = payment.cancellation_details.party
        return {
            "id": UUID(payment.id),
            "status": payment.status,
            "confirmation_url": confirmation_url,
            "payment_method_saved": payment_method_saved,
            "payment_method_id": payment_method_id,
            "cancellation_details_party": cancellation_details_party,
            "cancellation_details_reason": cancellation_details_reason,
        }

    def create_refund(self, data: InputRefundScheme) -> dict:
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
            return refund
        except BadRequestError as err:
            self.log.error("Не удалось создать возврат")
            raise HTTPException(
                status_code=404, detail="Failed to create refund"
            ) from err
