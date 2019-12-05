from app.boards.api.endpoints.boards_views import router as boards_router
from app.boards.api.endpoints.participants_views import router as participants_router
from app.boards.api.endpoints.column_views import router as columns_router
from fastapi import APIRouter


router = APIRouter()

router.include_router(boards_router)
router.include_router(participants_router)
router.include_router(columns_router)
