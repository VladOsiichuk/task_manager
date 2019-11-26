from fastapi import FastAPI, APIRouter

from app.auth.api.routing import router as auth_router
from app.boards.api.routing import router as boards_router
from app.core.config import DEBUG
from app.db.utils import close_connection, create_connection

api_router = APIRouter()
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(boards_router, prefix="/boards")

app = FastAPI(debug=DEBUG)

app.add_event_handler("startup", create_connection)
app.add_event_handler("shutdown", close_connection)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def index():
    return {"success": False}
