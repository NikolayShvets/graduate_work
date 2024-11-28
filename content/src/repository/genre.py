from models.models import Genre
from repository.base import SQLAlchemyRepository


class GenreRepository(SQLAlchemyRepository[Genre]):
    pass


genre_repository = GenreRepository(Genre)
