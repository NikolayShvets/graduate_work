from datetime import date
from uuid import UUID

from api.v1.schemas.base import Base


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

