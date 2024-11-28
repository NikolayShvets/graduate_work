from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.models import Person
from repository.base import SQLAlchemyRepository


class PersonRepository(SQLAlchemyRepository[Person]):
    async def search(self, session: AsyncSession, name):
        query = select(self._model).filter(Person.full_name.ilike(f'%{name}%'))

        return (await session.execute(query)).scalars().all()


person_repository = PersonRepository(Person)
