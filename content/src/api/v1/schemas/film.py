from datetime import date
from uuid import UUID

from api.v1.schemas.base import Base
from models.constance import VideoType


class FilmResponseSchema(Base):
    id: UUID
    title: str
    type: str
    imdb_rating: float | None
    creation_date: date | None
    description: str | None
    genres: str
    actors: list[dict[str, str | UUID]] | None
    directors: list[dict[str, str | UUID]] | None
    writers: list[dict[str, str | UUID]] | None


class FilmworkBaseSchema(Base):
    id: UUID
    title: str
    creation_date: date
    rating: float
    type: VideoType
    description: str | None = None
