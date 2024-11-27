from fastapi import APIRouter

from api.v1.routes.billing import router as billing_router

router = APIRouter(prefix="/api/billing/v1")

router.include_router(router=billing_router)
