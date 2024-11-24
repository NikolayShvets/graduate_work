from fastapi import APIRouter
from yookassa import Refund
from src.api.v1.schemas.schemas import (
    NewPayment as NewPaymentScheme,
    OutputNewPayment as OutputNewPaymentScheme,
    AutoPayment as AutoPaymentScheme,
    InputRefund as InputRefundScheme,
)

from src.services.billing import YooKassaBilling

router = APIRouter()
service_billing = YooKassaBilling()


@router.post("/create_payment", response_model=OutputNewPaymentScheme)
async def create_payment(data: NewPaymentScheme) -> OutputNewPaymentScheme:
    return service_billing.create_payment(data=data)


@router.post("/auto_payment", response_model=OutputNewPaymentScheme)
async def auto_payment(data: AutoPaymentScheme) -> OutputNewPaymentScheme:
    return service_billing.create_auto_payment(data=data)


@router.get("/checkout/{payment_id}")
async def checkout(payment_id: str) -> dict:
    return service_billing.get_payment(payment_id=payment_id)


@router.post("/refund/{payment_id}")
async def refund(data: InputRefundScheme) -> Refund:
    return service_billing.create_refund(data=data)
