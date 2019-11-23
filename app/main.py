from fastapi import FastAPI, Depends, APIRouter
from fastapi.security import HTTPBasic, HTTPBearer

from app.api.urls import router
from app.auth.api.routing import router as auth_router
from app.core.config import DEBUG

from app.db.utils import close_connection, create_connection

api_router = APIRouter()
api_router.include_router(router)
api_router.include_router(auth_router)

app = FastAPI(debug=DEBUG)

app.add_event_handler("startup", create_connection)
app.add_event_handler("shutdown", close_connection)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def index():
    return {"success": False}

