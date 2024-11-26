from fastapi import APIRouter
from yookassa import Refund
from src.api.v1.schemas.schemas import (
    NewPaymentScheme,
    OutputNewPaymentScheme,
    AutoPaymentScheme,
    InputRefundScheme,
)

from src.api.v1.deps.billing import Billing

router = APIRouter()


@router.post("/create_payment", response_model=OutputNewPaymentScheme)
async def create_payment(data: NewPaymentScheme, billing: Billing) -> OutputNewPaymentScheme:
    return billing.create_payment(data=data)


@router.post("/auto_payment", response_model=OutputNewPaymentScheme)
async def auto_payment(data: AutoPaymentScheme, billing: Billing) -> OutputNewPaymentScheme:
    return billing.create_auto_payment(data=data)


@router.get("/checkout/{payment_id}")
async def checkout(payment_id: str, billing: Billing) -> dict:
    return billing.get_payment(payment_id=payment_id)


@router.post("/refund/{payment_id}")
async def refund(data: InputRefundScheme, billing: Billing) -> Refund:
    return billing.create_refund(data=data)
