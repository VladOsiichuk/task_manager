import json

from fastapi import FastAPI, APIRouter
from fastapi.exceptions import RequestValidationError
from starlette.responses import PlainTextResponse

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


@app.exception_handler(RequestValidationError)
async def http_exception_handler(request, exc):
    error_body = {}
    errors = exc.errors()
    if isinstance(errors, list):
        for error in errors:
            error_body[error["loc"][-1]] = error["msg"]
    else:
        error_body[errors["loc"][-1]] = errors["msg"]
    return PlainTextResponse(json.dumps(error_body), status_code=400)


@app.get("/")
async def index():
    return {"success": False}
