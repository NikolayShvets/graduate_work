from fastapi import APIRouter

from api.v1.routes.film import router as film_router
from api.v1.routes.genre import router as genre_router
from api.v1.routes.person import router as person_router

router = APIRouter(prefix="/api/v1")

router.include_router(film_router, prefix="/film", tags=["Фильмы"])
router.include_router(genre_router, prefix="/genre", tags=["Жанры"])
router.include_router(person_router, prefix="/person", tags=["Персоны"])
