from app.boards.api.endpoints.boards_views import router as boards_router
from fastapi import APIRouter


router = APIRouter()
router.include_router(boards_router)
