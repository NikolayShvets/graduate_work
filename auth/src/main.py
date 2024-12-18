from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqladmin import Admin
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from admin.admin_auth import AdminAuth
from admin.role import RoleAdmin
from admin.user import UserAdmin
from admin.user_role import UserRoleAdmin
from api import v1_router
from db import postgresql, redis
from settings.api import settings as api_settings
from settings.postgresql import settings as postgresql_settings
from settings.redis import settings as redis_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    redis.redis_conn = Redis.from_url(redis_settings.DSN)
    postgresql.async_engine = create_async_engine(
        postgresql_settings.DSN,
        echo=postgresql_settings.LOG_QUERIES,
    )
    postgresql.async_session = async_sessionmaker(
        postgresql.async_engine, expire_on_commit=False
    )
    yield
    await redis.redis_conn.close()
    await postgresql.async_engine.dispose()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    root_path="/auth",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=api_settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)

postgresql.async_engine = create_async_engine(
    postgresql_settings.DSN,
    echo=postgresql_settings.LOG_QUERIES,
)

authentication_backend = AdminAuth(secret_key=api_settings.SECRET_KEY)
admin = Admin(
    app,
    postgresql.async_engine,
    title="Auth Admin",
    authentication_backend=authentication_backend,
)

admin.add_view(RoleAdmin)
admin.add_view(UserAdmin)
admin.add_view(UserRoleAdmin)
