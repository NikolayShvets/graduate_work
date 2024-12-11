from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from sqladmin import Admin
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from admin.admin_auth import AdminAuth
from admin.filmwork import FilmWorkAdmin
from admin.genre import GenreAdmin
from admin.genre_filmwork import GenreFilmWorkAdmin
from admin.person import PersonAdmin
from admin.person_filmwork import PersonFilmWorkAdmin
from api import v1_router
from db import postgresql
from settings.api import settings as api_settings
from settings.jwt import settings as jwt_settings
from settings.postgresql import settings as postgresql_settings


@asynccontextmanager
async def lifespan(_: FastAPI):
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
    root_path="/content",
)

app.include_router(v1_router)

postgresql.async_engine = create_async_engine(
    postgresql_settings.DSN,
    echo=postgresql_settings.LOG_QUERIES,
)

authentication_backend = AdminAuth(secret_key=jwt_settings.SECRET_KEY)
admin = Admin(
    app,
    postgresql.async_engine,
    title="Content Admin",
    authentication_backend=authentication_backend,
)

admin.add_view(GenreAdmin)
admin.add_view(FilmWorkAdmin)
admin.add_view(PersonAdmin)
admin.add_view(GenreFilmWorkAdmin)
admin.add_view(PersonFilmWorkAdmin)
