from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api import v1_router
from db import postgresql, redis
from settings.api import settings as api_settings
from settings.postgresql import settings as postgresql_settings
from settings.redis import settings as redis_settings
from settings.cors import settings as cors_settings


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
)

origins = [cors_settings.ORIGINS]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(v1_router)
