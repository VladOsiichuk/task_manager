from fastapi import APIRouter
from app.api.endpoints.projects import router as projects_router

router = APIRouter()

router.include_router(projects_router)
