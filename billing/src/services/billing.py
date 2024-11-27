from fastapi import HTTPException
from yookassa import Payment, Refund
import logging

from src.api.v1.schemas.schemas import (
    NewPaymentScheme,
    OutputNewPaymentScheme,
    AutoPaymentScheme,
    InputRefundScheme,
)

from yookassa.client import NotFoundError


class YooKassaBilling:
    """Класс биллинга YooKassa"""

    def __init__(self):
        self.log = logging.getLogger("main")

    def create_payment(self, data: NewPaymentScheme) -> OutputNewPaymentScheme:
        """
        Функция создает новый платеж.
        """
        try:
            payment = Payment.create({
                "amount": {
                    "value": data.amount,
                    "currency": data.currency,
                },
                "confirmation": {
                    "type": "redirect",
                    "return_url": "https://www.example.com/return_url"
                },
                "capture": True,
                "description": data.description,
                "save_payment_method": True
            })
            method_save = payment.payment_method.saved if hasattr(
                payment.payment_method, 'saved'
            ) else None
            method_id = payment.payment_method.id if hasattr(
                payment.payment_method, 'id'
            ) else None
            # здесь должна быть функция сохранения payment_method.id в бд для последующих автоплатежей
            return OutputNewPaymentScheme(
                id=payment.id,
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
            payment = Payment.create({
                "amount": {
                    "value": data.amount,
                    "currency": data.currency,
                },
                "capture": True,
                "payment_method_id": data.payment_method_id,
                "description": data.description,
            })
            confirmation_url = payment.confirmation.confirmation_url if hasattr(payment.confirmation,
                                                                                'confirmation_url') else None
            payment_method_saved = payment.payment_method.saved if hasattr(
                payment.payment_method, 'saved'
            ) else None
            payment_method_id = payment.payment_method.id if hasattr(
                payment.payment_method, 'id'
            ) else None
            # здесь должна быть функция сохранения payment_method.id в бд для последующих автоплатежей
            return OutputNewPaymentScheme(
                id=payment.id,
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
            self.log.error('Item not found')
            raise HTTPException(status_code=404, detail="Item not found")

        confirmation_url = payment.confirmation.confirmation_url if hasattr(payment.confirmation,
                                                                            'confirmation_url') else None
        payment_method_saved = payment.payment_method.saved if hasattr(
            payment.payment_method, 'saved'
        ) else None
        payment_method_id = payment.payment_method.id if hasattr(
            payment.payment_method, 'id'
        ) else None
        cancellation_details_party = payment.cancellation_details.party if hasattr(payment.cancellation_details,
                                                                                   'party') else None
        cancellation_details_reason = payment.cancellation_details.party if hasattr(payment.cancellation_details,
                                                                                    'reason') else None
        return {
            'id': payment.id,
            'status': payment.status,
            'confirmation_url': confirmation_url,
            'payment_method_saved': payment_method_saved,
            'payment_method_id': payment_method_id,
            'cancellation_details_party': cancellation_details_party,
            'cancellation_details_reason': cancellation_details_reason,
        }

    def create_refund(self, data: InputRefundScheme) -> Refund:
        """
            Создает возврат средств.
        """
        refund = Refund.create({
            "amount": {
                "value": data.amount,
                "currency": data.currency,
            },
            "payment_id": data.payment_id
        })
        return refund
