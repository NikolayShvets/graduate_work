from typing import Annotated, Literal
from uuid import UUID

from fastapi import APIRouter, HTTPException, status, Query

from src.api.v1.deps.session import Session
from src.api.v1.deps.user import UserData
from src.api.v1.schemas.film import FilmResponseSchema
from src.repository.film import film_repository
from src.services.data_transfer import DataTransform


router = APIRouter()
data_transformer = DataTransform()


@router.get("/{film_id}")
async def retrieve(
        film_id: UUID,
        session: Session,
        user: UserData,
) -> FilmResponseSchema:
    """
    Получить полную информацию о фильме по его идентификатору.
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
            Query(description="Указывает поле для сортировки фильмов.")
        ],
        genre: str | None = Query(None, description="Фильтрует фильмы по жанру.")
) -> list[FilmResponseSchema]:
    """
    Получить список фильмов с возможностью фильтрации и сортировки.
    Возвращает список фильмов.
    - **sort**: Сортировка
    - **genre**: Жанр
    """
    obj = await film_repository.get_all_films_info(session, sort=sort, genre=genre)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Films not found"
        )

    data = await data_transformer.transform_movies_pgdata(obj)
    films = [FilmResponseSchema(**film) for film in data]

    return films


@router.get("/search/")
async def search(
        title: str | None,
        session: Session,
        user: UserData
) -> list[FilmResponseSchema]:
    """
    Возвращает список фильмов по заданному названию.
    - **title**: Заголовок фильма для поиска
    """
    obj = await film_repository.search(session, title)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Films not found"
        )

    data = await data_transformer.transform_movies_pgdata(obj)

    films = [FilmResponseSchema(**film) for film in data]

    return films


