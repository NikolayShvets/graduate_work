from uuid import UUID

from pydantic import Field

from src.api.v1.schemas.base import Base


class GenreResponseSchema(Base):
    id: UUID = Field(..., title="UUID", description="Идентификатор жанра")
    name: str = Field(..., title="Имя", description="Название жанра")
    description: str | None = Field(
        None, title="Описание", description="Описание жанра"
    )
