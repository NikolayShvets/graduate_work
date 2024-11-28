from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from repository.genre import genre_repository
from api.v1.schemas.genre import GenreResponseSchema
from api.v1.deps.user import UserData


router = APIRouter()


@router.get("/{genre_id}/")
async def retrieve(
        session: Session,
        genre_id: UUID,
        user: UserData
) -> GenreResponseSchema:
    """
    Получение информации о жанре по его идентификатору.
    - **genre_id**: Уникальный идентификатор жанра (обязательный параметр пути).
    Возвращает полную информацию о жанре.
    """

    genre = await genre_repository.get(session, id=genre_id)

    if genre is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genre not found"
        )

    return genre


@router.get("/")
async def retrieve_all(
        session: Session,
        user: UserData
) -> list[GenreResponseSchema]:
    """
    Получение всех жанров.
    Возвращает список жанров.
    """

    obj_list = await genre_repository.filter(session)

    if obj_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Genres not found"
        )

    genres = [GenreResponseSchema(**genre.to_dict()) for genre in obj_list]

    return genres
