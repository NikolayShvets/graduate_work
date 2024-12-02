from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.deps.user import UserData
from api.v1.schemas.person import PersonResponseSchema
from repository.person import person_repository

router = APIRouter()


@router.get("/search/")
async def search(
    name: str | None, session: Session, user: UserData
) -> list[PersonResponseSchema]:
    """
    Поиск персоны по имени.
    Возвращает список персон по заданному имени.
    """
    obj = await person_repository.search(session, name)

    if obj is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persons not found"
        )

    persons = [PersonResponseSchema(**person.to_dict()) for person in obj]

    return persons


@router.get("/{person_id}/")
async def details(
    session: Session, person_id: UUID, user: UserData
) -> PersonResponseSchema:
    """
    Получение информации о персоне по ее идентификатору.
    - **person_id**: Уникальный идентификатор персоны (обязательный параметр пути).
    Возвращает информацию о персоне.
    """
    person = await person_repository.get(session, id=person_id)

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Person not found"
        )

    return person


@router.get("/")
async def get_all(session: Session, user: UserData) -> list[PersonResponseSchema]:
    """
    Получение списка персон.
    Возвращает список персон.
    """
    obj_list = await person_repository.filter(session)

    if obj_list is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Persons not found"
        )

    persons = [PersonResponseSchema(**person.to_dict()) for person in obj_list]

    return persons
