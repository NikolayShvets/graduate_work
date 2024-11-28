from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from models.models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    Person,
    PersonFilmWork,
)
from repository.base import SQLAlchemyRepository


class FilmRepository(SQLAlchemyRepository[FilmWork]):
    @staticmethod
    async def get_all_films_info(session: AsyncSession, sort=None, genre=None, film_id=None):
        pfw = aliased(PersonFilmWork)
        gfw = aliased(GenreFilmWork)

        query = (select(
            FilmWork.id.label("fw_id"),
            FilmWork.title,
            FilmWork.description,
            FilmWork.rating,
            FilmWork.type,
            FilmWork.creation_date,
            pfw.role,
            Person.id.label("person_id"),
            Person.full_name,
            Genre.name,
            Genre.id.label("genre_id"),
        )
         .join(pfw, pfw.film_work_id == FilmWork.id)
         .join(Person, Person.id == pfw.person_id)
         .join(gfw, gfw.film_work_id == FilmWork.id)
         .join(Genre, Genre.id == gfw.genre_id))

        if sort is not None:
            query = query.order_by(sort)

        if genre is not None:
            query = query.where(Genre.name == genre)

        if film_id is not None:
            query = query.where(FilmWork.id == film_id)

        return (await session.execute(query)).mappings().all()

    @staticmethod
    async def search(session: AsyncSession, title):
        pfw = aliased(PersonFilmWork)
        gfw = aliased(GenreFilmWork)

        query = ((select(
            FilmWork.id.label("fw_id"),
            FilmWork.title,
            FilmWork.description,
            FilmWork.rating,
            FilmWork.type,
            FilmWork.creation_date,
            pfw.role,
            Person.id.label("person_id"),
            Person.full_name,
            Genre.name,
            Genre.id.label("genre_id"),
        )
         .join(pfw, pfw.film_work_id == FilmWork.id)
         .join(Person, Person.id == pfw.person_id)
         .join(gfw, gfw.film_work_id == FilmWork.id)
         .join(Genre, Genre.id == gfw.genre_id))
         .filter(FilmWork.title.ilike(f'%{title}%')))

        return (await session.execute(query)).mappings().all()


film_repository = FilmRepository(FilmWork)



