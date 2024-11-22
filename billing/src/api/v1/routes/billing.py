from fastapi import HTTPException, APIRouter
from yookassa import Payment
from src.api.v1.schemas.schemas import (
    NewPayment as NewPaymentScheme,
    OutputNewPayment as OutputNewPaymentScheme,
    AutoPayment as AutoPaymentScheme,
)
from src.logger.logger import logger
from yookassa.client import NotFoundError

router = APIRouter()


@router.post("/new_payment", response_model=OutputNewPaymentScheme)
async def new_payment(data: NewPaymentScheme) -> OutputNewPaymentScheme:
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
        logger.error(e)


@router.post("/auto_payment")
async def auto_payment(data: AutoPaymentScheme):
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
        logger.error(e)


@router.get("/checkout/{payment_id}")
async def checkout(payment_id: str):
    try:
        payment = Payment.find_one(payment_id)
        confirmation_url = payment.confirmation.confirmation_url if hasattr(payment.confirmation,
                                                                            'confirmation_url') else None
        payment_method_saved = payment.payment_method.saved if hasattr(
            payment.payment_method, 'saved'
        ) else None
        payment_method_id = payment.payment_method.id if hasattr(
            payment.payment_method, 'id'
        ) else None
        cancellation_details = payment.cancellation_details.party if hasattr(payment.cancellation_details,
                                                                             'party') else None
        return {
            'id': payment.id,
            'status': payment.status,
            'confirmation_url': confirmation_url,
            'payment_method_saved': payment_method_saved,
            'payment_method_id': payment_method_id,
            'cancellation_details': cancellation_details,
        }
    except NotFoundError:
        return {'status': 404, 'detail': "Платеж не найден"}
