from fastapi import Request
from sqladmin.authentication import AuthenticationBackend

from api.v1.deps.user import check_admin, check_login, logout


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)

    @staticmethod
    async def get_credentials(request: Request) -> dict[str, str]:
        form = await request.form()
        data = {"username": form["username"], "password": form["password"]}
        return data

    async def login(self, request: Request) -> bool:
        credentials = await self.get_credentials(request)
        tokens = await check_login(credentials)

        request.session.update({"token": tokens["access_token"]})
        return True

    async def logout(self, request: Request) -> bool:
        token = request.session.get("token")
        await logout(token)

        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        await check_admin(token)

        return True
