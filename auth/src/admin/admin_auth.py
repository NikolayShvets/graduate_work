from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi_users.authentication.authenticator import Authenticator

from api.v1.routes.auth import login, logout, check
from api.v1.deps.fastapi_users import (
    OAuth2Credentials,
    authentication_backend,
    get_user_manager,
    get_user_db,
    fastapi_users, CurrentUser
)
from api.v1.deps.user_agent import get_user_agent
from users.strategy import AccessJWTStrategy, RefreshJWTStrategy
from settings.postgresql import settings
from admin.clients.auth.client import auth_client


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self.async_session: AsyncSession | None = None
        self.init_session()

    def init_session(self):
        async_engine = create_async_engine(settings.DSN, echo=settings.LOG_QUERIES)
        self.async_session = async_sessionmaker(async_engine, expire_on_commit=False)

    @staticmethod
    async def get_user_agent(request: Request) -> str:
        return get_user_agent(request)

    @staticmethod
    async def get_user_manager(session: AsyncSession) -> SQLAlchemyUserDatabase:
        user_db = await anext(get_user_db(session))
        return await anext(get_user_manager(user_db))

    @staticmethod
    async def get_access_strategy() -> AccessJWTStrategy:
        return authentication_backend.get_strategy()

    @staticmethod
    async def get_refresh_strategy() -> RefreshJWTStrategy:
        return authentication_backend.get_refresh_strategy()

    @staticmethod
    async def get_credentials(request: Request) -> OAuth2PasswordRequestForm:
        form = await request.form()
        return OAuth2Credentials(username=form["username"], password=form["password"])

    @staticmethod
    async def get_current_user_token(user_manager) -> tuple:
        fastapi_users.authenticator.get_user_manager = user_manager
        token = (fastapi_users.current_user_to(active=True))
        print(3333, token)

        t = await token()
        return t

    async def login(self, request: Request) -> bool:
        async with self.async_session() as session:
            payload = {
                "user_agent": await self.get_user_agent(request),
                "user_manager": await self.get_user_manager(session),
                "access_strategy": await self.get_access_strategy(),
                "refresh_strategy": await self.get_refresh_strategy(),
                "session": session,
                "credentials": await self.get_credentials(request)
            }

        user = await login(**payload)
        request.session.update({"token": user.access_token})

        return True

    async def logout(self, request: Request) -> bool:
        print(f'\nin admin_logout()')
        token = request.session.get("token")
        print(f'\ttoken:{token}')
        user = await auth_client.check(token)
        print(f'\tuser: {user}')

        async with self.async_session() as session:
            payload = {
                "user_token": (user, token),
                "user_agent": await self.get_user_agent(request),
                "access_strategy": await self.get_access_strategy(),
                "refresh_strategy": await self.get_refresh_strategy(),
                "session": session,
            }
            # print(f'\tuser_token: {payload['user_token']}')
        await logout(**payload)

        request.session.clear()

        return True

    async def authenticate(self, request: Request) -> bool:
        # TODO: проверку роли, что админ; проверка токена
        print(f'\nin authenticate()')
        token = request.session.get("token")
        print(f'\ttoken: {token}')

        if not token:
            return False

        # Check the token in depth
        return True

