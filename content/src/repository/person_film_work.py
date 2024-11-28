from models.models import PersonFilmWork
from repository.base import SQLAlchemyRepository


class PersonFilmWorkRepository(SQLAlchemyRepository[PersonFilmWork]):
    pass


person_fw_repository = PersonFilmWorkRepository(PersonFilmWork)
