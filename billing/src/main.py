from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from yookassa import Configuration

from api import v1_router
from db import postgresql
from settings.api import settings as api_settings
from settings.postgresql import settings as postgresql_settings
from settings.yookassa import settings as yookassa_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    Configuration.configure(
        account_id=yookassa_settings.ACCOUNT_ID,
        secret_key=yookassa_settings.KASSA_SECRET_KEY.get_secret_value(),
    )
    postgresql.async_engine = create_async_engine(
        postgresql_settings.DSN,
        echo=postgresql_settings.LOG_QUERIES,
    )
    postgresql.async_session = async_sessionmaker(
        postgresql.async_engine, expire_on_commit=False
    )
    yield
    await postgresql.async_engine.dispose()


app = FastAPI(
    title=api_settings.TITLE,
    openapi_url=api_settings.OPENAPI_URL,
    docs_url=api_settings.DOCS_URL,
    redoc_url=api_settings.REDOC_URL,
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
    root_path=api_settings.ROOT_PATH,
)

app.include_router(v1_router)
