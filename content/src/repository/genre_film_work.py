from src.models.models import GenreFilmWork
from src.repository.base import SQLAlchemyRepository


class GenreFilmWorkRepository(SQLAlchemyRepository[GenreFilmWork]):
    pass


genre_fw_repository = GenreFilmWorkRepository(GenreFilmWork)
