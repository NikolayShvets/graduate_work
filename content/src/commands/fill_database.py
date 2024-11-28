import asyncio
import datetime
import logging
from random import randint, choice

import asyncpg
import sqlalchemy
from faker import Faker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from settings.postgresql import settings
from settings.logger import settings as log_settings
from db import postgresql
from repository.genre import genre_repository
from repository.person import person_repository
from repository.film import film_repository
from repository.genre_film_work import genre_fw_repository
from repository.person_film_work import person_fw_repository
from models.constance import VideoType, Role


logger = logging.getLogger(log_settings.LOG_NAME)
faker = Faker()
GENRES = ['Комедия', 'Фантастика', 'Ужасы', 'Боевик', 'Мелодрама', 'Мистика', 'Детектив']


postgresql.async_engine = create_async_engine(
        settings.DSN,
        echo=settings.LOG_QUERIES,
    )
postgresql.async_session = async_sessionmaker(
    postgresql.async_engine, expire_on_commit=False
)


async def fill_genres():
    id_list = []
    async with postgresql.async_session() as session:
        for genre in GENRES:
            obj = await genre_repository.create(session, data={"name": genre})
            id_list.append(obj.id)
    return id_list


async def fill_persons():
    id_list = []
    async with postgresql.async_session() as session:
        for _ in range(7):
            obj = await person_repository.create(session, data={"full_name": faker.name()})
            id_list.append(obj.id)
    return id_list


async def fill_films():
    id_list = []
    films = [
        {
            "title": faker.text(randint(10, 30)),
            "rating": randint(1, 10),
            "type": choice([VideoType.MOVIE.name, VideoType.TV_SHOW.name]),
            "creation_date": faker.date_between(datetime.date(1950, 1, 1), datetime.date(2023, 1, 1))
        } for _ in range(7)
    ]

    async with postgresql.async_session() as session:
        for film in films:
            obj = await film_repository.create(session, data=film)
            id_list.append(obj.id)
    return id_list


async def fill_genre_film_work(genre_id_list, film_id_list):
    genre_fw_id_list = zip(genre_id_list, film_id_list)

    async with postgresql.async_session() as session:
        for id_ in genre_fw_id_list:
            data = {
                "genre_id": id_[0],
                "film_work_id": id_[1]
            }
            await genre_fw_repository.create(session, data=data)


async def fill_person_film_work(person_id_list, film_id_list):
    person_fw_id_list = zip(person_id_list, film_id_list)

    async with postgresql.async_session() as session:
        for id_ in person_fw_id_list:
            data = {
                "person_id": id_[0],
                "film_work_id": id_[1],
                "role": choice([Role.ACTOR.name, Role.WRITER.name, Role.DIRECTOR.name])
            }
            await person_fw_repository.create(session, data=data)


async def main():
    try:
        logger.info('Filling Postgres database with test data')
        genre_id_list = await fill_genres()
        person_id_list = await fill_persons()
        film_id_list = await fill_films()

        await fill_genre_film_work(genre_id_list, film_id_list)
        await fill_person_film_work(person_id_list, film_id_list)

        logger.info('End of filling database')
    except sqlalchemy.exc.IntegrityError:
        logger.info('Database is already full')


if __name__ == '__main__':
    asyncio.run(main())
