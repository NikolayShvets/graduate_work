from clients.auth.schemas import UserRetrieveSchema
from clients.base.client import BaseClient
from settings.api import settings


class AuthClient(BaseClient):
    async def check(self, token: str) -> UserRetrieveSchema:
        user = await self._post(
            url="/jwt/check", headers={"Authorization": f"Bearer {token}"}
        )
        return UserRetrieveSchema.model_validate(user)


auth_client = AuthClient(base_url=f"{settings.AUTH_API_URL}/auth/api/v1")
