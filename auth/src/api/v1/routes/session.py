from fastapi import APIRouter

from api.v1.deps.fastapi_users import CurrentUser, Session
from api.v1.schemas.session import SessionRetrieveSchema
from repository.session import session_repository

router = APIRouter()


@router.get("/history")
async def get_history(
    user: CurrentUser, session: Session
) -> list[SessionRetrieveSchema]:
    """Получение истории входов пользователя в аккаунт."""
    return await session_repository.get_history(session, user.id)
