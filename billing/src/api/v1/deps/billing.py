from typing import Annotated

from fastapi import Depends

from src.services.billing import YooKassaBilling


def get_billing_service() -> YooKassaBilling:
    return YooKassaBilling()


Billing = Annotated[YooKassaBilling, Depends(get_billing_service)]
