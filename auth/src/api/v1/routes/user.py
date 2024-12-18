from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.schemas.user import UserRetrieveSchema
from repository.user import user_repository

router = APIRouter()


@router.get("/{user_id}")
async def retrieve(session: Session, user_id: UUID) -> UserRetrieveSchema:
    """Просмотр пользователя."""

    user = await user_repository.get(session, id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return user
