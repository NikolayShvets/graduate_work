from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from api.v1.deps.session import Session
from api.v1.deps.user import User
from api.v1.schemas.tariff import TariffRetrieveSchema
from repository.tariff import tariff_repository

router = APIRouter()


@router.get("/tariffs")
async def retrive_all(session: Session, _: User) -> list[TariffRetrieveSchema]:
    """Получить все тарифы."""

    return await tariff_repository.filter(session=session)


@router.get("/tariffs/{tariff_id}")
async def retrive_one(
    session: Session, tariff_id: UUID, _: User
) -> TariffRetrieveSchema:
    """Получить тариф."""

    tariff = await tariff_repository.get(session=session, id=tariff_id)

    if tariff is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return tariff
