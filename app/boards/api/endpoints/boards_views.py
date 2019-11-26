from fastapi import APIRouter, Depends

from app.auth.jwt_auth import jwt_auth
from app.boards.models.boards_models import (
    BoardCreateRequestModel,
    BoardCreateResponseModel,
)
from app.core.pydantic.models import ExceptionModel
from app.db.models import Board

router = APIRouter()


@router.post(
    "/",
    response_model=BoardCreateResponseModel,
    status_code=201,
    responses={"401": {"model": ExceptionModel}},
)
async def create_board(data: BoardCreateRequestModel, author=Depends(jwt_auth)):

    board_name = data.name
    author_id = author.id

    board = Board(name=board_name, author_id=author_id)
    await board.create()

    setattr(board, "author", author)

    return BoardCreateResponseModel.from_orm(board)
