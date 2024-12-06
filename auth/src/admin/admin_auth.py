from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users.router.common import ErrorCode
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import joinedload

from api.v1.deps.fastapi_users import (
    OAuth2Credentials,
    get_user_db,
    get_user_manager,
)
from models.models import User, UserRole
from repository.user import user_repository
from settings.postgresql import settings


class AdminAuth(AuthenticationBackend):
    def __init__(self, secret_key: str):
        super().__init__(secret_key=secret_key)
        self._async_session: AsyncSession | None = None
        self._allowed_roles: list[str] = ['admin']

        self.init_session()

    def init_session(self):
        async_engine = create_async_engine(settings.DSN, echo=settings.LOG_QUERIES)
        self._async_session = async_sessionmaker(async_engine, expire_on_commit=False)

    @staticmethod
    async def get_user_manager(session: AsyncSession) -> SQLAlchemyUserDatabase:
        user_db = await anext(get_user_db(session))
        return await anext(get_user_manager(user_db))

    @staticmethod
    async def get_credentials(request: Request) -> OAuth2PasswordRequestForm:
        form = await request.form()
        return OAuth2Credentials(username=form["username"], password=form["password"])

    async def login(self, request: Request) -> bool:
        async with self.async_session() as session:
            user_manager = await self.get_user_manager(session)

        credentials = await self.get_credentials(request)
        user = await user_manager.authenticate(credentials=credentials)

        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorCode.LOGIN_BAD_CREDENTIALS,
            )
        request.session.update({"token": str(user.id)})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        async with self.async_session() as session:
            user = await user_repository.get(
                session, id=token, options=[joinedload(User.roles).joinedload(UserRole.role)]
            )

        role_names = {user_role.role.name for user_role in user.roles}

        if not role_names.intersection(self._allowed_roles) and not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )

        return True
