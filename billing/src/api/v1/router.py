from fastapi import APIRouter

from api.v1.routes.subscription import router as subscription_router
from api.v1.routes.tariff import router as tariff_router
from api.v1.routes.yookassa import router as yookassa_router

router = APIRouter(prefix="/api/billing/v1")

router.include_router(
    router=subscription_router, prefix="/subscriptions", tags=["Подписки"]
)
router.include_router(router=tariff_router, prefix="/tariffs", tags=["Тарифы"])
router.include_router(router=yookassa_router, prefix="/yookassa", tags=["YooKassa"])
