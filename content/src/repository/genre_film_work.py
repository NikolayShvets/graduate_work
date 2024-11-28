from models.models import GenreFilmWork
from repository.base import SQLAlchemyRepository


class GenreFilmWorkRepository(SQLAlchemyRepository[GenreFilmWork]):
    pass


genre_fw_repository = GenreFilmWorkRepository(GenreFilmWork)
