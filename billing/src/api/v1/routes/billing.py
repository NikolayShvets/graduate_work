from fastapi import APIRouter

from api.v1.deps.billing import Billing
from api.v1.schemas.schemas import (
    AutoPaymentScheme,
    InputRefundScheme,
    NewPaymentScheme,
    OutputPaymentScheme,
    OutputRefundScheme,
)

router = APIRouter()


@router.post("/create_payment", response_model=OutputPaymentScheme)
async def create_payment(
    data: NewPaymentScheme, billing: Billing
) -> OutputPaymentScheme:
    result = billing.create_payment(data=data)
    return OutputPaymentScheme(**result.dict())


@router.post("/auto_payment", response_model=OutputPaymentScheme)
async def auto_payment(
    data: AutoPaymentScheme, billing: Billing
) -> OutputPaymentScheme:
    result = billing.create_auto_payment(data=data)
    return OutputPaymentScheme(**result.dict())


@router.get("/checkout/{payment_id}")
async def checkout(payment_id: str, billing: Billing) -> OutputPaymentScheme:
    result = billing.get_payment(payment_id=payment_id)
    return OutputPaymentScheme(**result.dict())


@router.post("/refund/{payment_id}")
async def refund(data: InputRefundScheme, billing: Billing):
    result = billing.create_refund(data=data)
    return OutputRefundScheme(**result.dict())
