from uuid import UUID

from fastapi import APIRouter, Depends
from app.boards.models.column_models import (
    ColumnCreateRequestModel,
    ColumnCreateResponseModel,
)
from app.core.dependencies import is_board_moderator
from app.db.models import Board, BoardColumn

router = APIRouter()


@router.post(
    "/{board_uuid}/columns/", status_code=201, response_model=ColumnCreateResponseModel
)
async def create_column(
    board_uuid: UUID, data: ColumnCreateRequestModel, __=Depends(is_board_moderator)
):

    board = await Board.query.where(Board.uuid == board_uuid).gino.first()

    column = BoardColumn(board_id=board.id, name=data.name)
    await column.create()
    return ColumnCreateResponseModel.from_orm(column)
