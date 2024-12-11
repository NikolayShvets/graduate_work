from clients.auth.schemas import UserRetrieveSchema
from clients.base.client import BaseClient
from settings.api import settings


class AuthClient(BaseClient):
    async def check(self, token: str) -> UserRetrieveSchema:
        user = await self._get(
            url="/jwt/check", headers={"Authorization": f"Bearer {token}"}
        )
        return UserRetrieveSchema.model_validate(user)

    async def check_admin(self, token: str) -> UserRetrieveSchema:
        return await self._get(
            url="/jwt/check_admin", headers={"Authorization": f"Bearer {token}"}
        )

    async def login(self, credentials: dict[str, str]) -> dict[str, str]:
        return await self._post(url="/jwt/login", data=credentials)

    async def logout(self, token: str):
        return await self._post(
            url="/jwt/logout", headers={"Authorization": f"Bearer {token}"}
        )


auth_client = AuthClient(base_url=f"{settings.AUTH_API_URL}/auth/api/v1")
