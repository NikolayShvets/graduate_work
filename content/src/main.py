from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqladmin import Admin

from api import v1_router
from db import postgresql
from settings.api import settings as api_settings
from settings.postgresql import settings as postgresql_settings
from admin.genre import GenreAdmin
from admin.filmwork import FilmAdmin
from admin.person import PersonAdmin
from admin.genre_filmwork import GenreFilmWorkAdmin
from admin.person_filmwork import PersonFilmWorkAdmin


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

admin = Admin(app, postgresql.async_engine, title="Content Admin")

admin.add_view(GenreAdmin)
admin.add_view(FilmAdmin)
admin.add_view(PersonAdmin)
admin.add_view(GenreFilmWorkAdmin)
admin.add_view(PersonFilmWorkAdmin)
