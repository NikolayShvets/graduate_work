from src.models.models import PersonFilmWork
from src.repository.base import SQLAlchemyRepository


class PersonFilmWorkRepository(SQLAlchemyRepository[PersonFilmWork]):
    pass


person_fw_repository = PersonFilmWorkRepository(PersonFilmWork)
