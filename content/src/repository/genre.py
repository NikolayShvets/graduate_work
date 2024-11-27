from src.models.models import Genre
from src.repository.base import SQLAlchemyRepository


class GenreRepository(SQLAlchemyRepository[Genre]):
    pass


genre_repository = GenreRepository(Genre)
