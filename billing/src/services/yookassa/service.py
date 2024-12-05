import asyncio
from collections.abc import Callable
from typing import Any
from uuid import UUID

from yookassa import Payment as YooPayment
from yookassa.client import NotFoundError
from yookassa.domain.response import PaymentResponse

from logger import logger
from services.yookassa.dto.amount import Amount
from services.yookassa.dto.confirmation import Confirmation
from services.yookassa.dto.payment import Payment


class YooKassa:
    @staticmethod
    async def _run_sync_async(func: Callable, *args) -> Any:
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)

    async def create_recurrent_payment(
        self,
        amount: Amount,
        confirmation: Confirmation,
        description: str,
    ) -> Payment:
        data = {
            "amount": {
                "value": amount.value,
                "currency": amount.currency,
            },
            "confirmation": {
                "type": confirmation.type,
                "return_url": confirmation.return_url,
            },
            "description": description,
            "capture": True,
            "save_payment_method": True,
        }

        try:
            payment: PaymentResponse = await self._run_sync_async(
                YooPayment.create, data
            )
        except Exception as e:
            logger.exception("Error creating recurrent payment: %s", e)
            raise

        return Payment.model_validate(payment)

    async def create_auto_payment(
        self, amount: Amount, description: str, payment_method_id: UUID
    ) -> Payment:
        data = {
            "amount": {
                "value": amount.value,
                "currency": amount.currency,
            },
            "description": description,
            "capture": True,
            "payment_method_id": str(payment_method_id),
        }

        try:
            payment: PaymentResponse = await self._run_sync_async(
                YooPayment.create, data
            )
        except Exception as e:
            logger.exception("Error creating auto payment: %s", e)
            raise

        return Payment.model_validate(payment)

    async def get_payment(self, payment_id: UUID) -> Payment:
        try:
            payment: PaymentResponse = await self._run_sync_async(
                YooPayment.find_one, str(payment_id)
            )
        except NotFoundError as e:
            logger.exception("Error getting payment: %s", e)
            raise e

        return Payment.model_validate(payment)
