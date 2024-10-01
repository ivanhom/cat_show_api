from fastapi import APIRouter

from api.api_v1.breed import router as breed_router
from api.api_v1.cat import router as cat_router


router = APIRouter(
    prefix='/v1',
)

router.include_router(breed_router, prefix='/breeds')
router.include_router(cat_router, prefix='/cats')
