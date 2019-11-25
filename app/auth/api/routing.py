from fastapi import APIRouter
from app.auth.api.endpoints.auth_views import router as auth_router
from app.auth.api.endpoints.token_views import router as token_router

router = APIRouter()

router.include_router(auth_router)
router.include_router(token_router, prefix="/token")
