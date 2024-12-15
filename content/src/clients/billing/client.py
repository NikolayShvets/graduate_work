from uuid import UUID

from clients.base.client import BaseClient
from clients.base.exceptions import NotFoundError
from settings.api import settings


class BillingClient(BaseClient):
    async def movie_is_available(self, user_id: UUID, movie_id: UUID) -> bool:
        """Проверить, доступен ли фильм для просмотра."""

        try:
            await self._get(url=f"/subscriptions/{user_id}/{movie_id}")
        except NotFoundError:
            return False
        return True


billing_client = BillingClient(base_url=f"{settings.BILLING_API_URL}/billing/api/v1")
