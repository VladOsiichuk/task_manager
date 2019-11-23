from fastapi import APIRouter
from app.auth.api.endpoints.register_view import router as register_router

router = APIRouter()

router.include_router(register_router, prefix="/auth")
