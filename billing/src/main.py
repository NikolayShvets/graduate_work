from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from yookassa import Configuration

from src.api import v1_router
from src.db import postgresql
from src.settings.api import settings as api_settings
from src.settings.postgresql import settings as postgresql_settings
from src.settings.yookassa import settings as yookassa_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
    Configuration.account_id = yookassa_settings.ACCOUNT_ID
    Configuration.secret_key = yookassa_settings.KASSA_SECRET_KEY
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
)

app.include_router(v1_router)
