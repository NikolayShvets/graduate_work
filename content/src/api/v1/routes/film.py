from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, Query, status

from api.v1.deps.session import Session
from api.v1.deps.user import UserData
from api.v1.schemas.film import FilmResponseSchema
from repository.film import film_repository
from services.data_transfer import DataTransform

router = APIRouter()
data_transformer = DataTransform()


@router.get("/search/")
async def search(
    title: str | None, session: Session, user: UserData
) -> list[FilmResponseSchema]:
    """
    Поиск фильма по названию.
    Возвращает список фильмов по заданному названию.
    """
    obj = await film_repository.search(session, title)

    if len(obj) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Films not found"
        )

    data = await data_transformer.transform_movies_pgdata(obj)

    films = [FilmResponseSchema(**film) for film in data]

    return films


@router.get("/{film_id}/")
async def retrieve(
    film_id: UUID,
    session: Session,
    user: UserData,
) -> FilmResponseSchema:
    """
    Получение полной информации о фильме по его идентификатору.
    - **film_id**: Уникальный идентификатор фильма (обязательный параметр пути).
    Возвращает полную информацию о фильме в случае успеха,
    """
    film = await film_repository.get_all_films_info(session, film_id=film_id)

    if not film:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Film not found"
        )

    data = await data_transformer.transform_movies_pgdata(film)

    return FilmResponseSchema(**data[0])


@router.get("/")
async def retrieve_all(
    session: Session,
    user: UserData,
    sort: Annotated[
        Literal["rating", "creation_date"] | None,
        Query(description="Указывает поле для сортировки фильмов."),
    ],
    genre: str | None = Query(None, description="Фильтрует фильмы по жанру."),
) -> list[FilmResponseSchema]:
    """
    Получение списка фильмов с возможностью фильтрации и сортировки.
    Возвращает список фильмов.
    - **sort**: Сортировка
    - **genre**: Жанр
    """
    obj = await film_repository.get_all_films_info(session, sort=sort, genre=genre)

    if len(obj) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Films not found"
        )

    data = await data_transformer.transform_movies_pgdata(obj)
    films = [FilmResponseSchema(**film) for film in data]

    return films
