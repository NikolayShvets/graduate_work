import asyncio
from uuid import UUID

from yookassa import Payment as YooPayment
from yookassa.client import NotFoundError
from yookassa.domain.response import PaymentResponse

from services.billing.dto.amount import Amount
from services.billing.dto.confirmation import Confirmation
from services.billing.dto.payment import Payment


class YooKassa:
    async def create_payment(
        self,
        amount: Amount,
        auto_payment: bool = False,
        confirmation: Confirmation | None = None,
    ) -> Payment:
        loop = asyncio.get_running_loop()

        data = {
            "amount": {
                "value": amount.value,
                "currency": amount.currency,
            },
        }

        if confirmation:
            data["confirmation"] = {
                "type": confirmation.type,
                "return_url": confirmation.return_url,
            }

        if auto_payment:
            data["save_payment_method"] = True

        payment: PaymentResponse = await loop.run_in_executor(
            None,
            YooPayment.create,
            data,
        )

        return Payment.model_validate(payment)

    async def get_payment(self, payment_id: UUID) -> Payment:
        loop = asyncio.get_running_loop()

        try:
            payment = await loop.run_in_executor(
                None, YooPayment.find_one, str(payment_id)
            )
        except NotFoundError as e:
            self.log.error("Item not found")
            # TODO: add custom exception
            raise e

        return Payment.model_validate(payment)
