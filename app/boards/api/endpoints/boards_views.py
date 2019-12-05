from itertools import groupby
from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.requests import Request

from app.auth.jwt_auth import jwt_auth
from app.boards.models.boards_models import (
    BoardCreateRequestModel,
    BoardCreateResponseModel,
    BoardListResponseModel,
    BoardQueryParamsModel,
)
from app.core.pydantic.models import ExceptionModel
from app.crud.board_queries import BoardListFilterQuery, BoardWithColumnsQueryFilter
from app.crud.utils import group_by, many_group_by
from app.db.models import Board, UserOnBoard, User
from app.db.models import db
from app.core.dependencies import has_common_board_access

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
    user_relation = UserOnBoard(
        user_id=author_id, board_id=board.id, role=UserOnBoard.ADMIN
    )
    await user_relation.create()

    board = await Board.load(author=User).query.where(Board.id == board.id).gino.first()
    return BoardCreateResponseModel.from_orm(board)


@router.get(
    "/",
    status_code=200,
    responses={401: {"model": ExceptionModel}},
    response_model=BoardListResponseModel,
)
async def boards_list(request: Request, user=Depends(jwt_auth)):
    query = BoardListFilterQuery.get_query_with_filters(
        request=request, model=BoardQueryParamsModel, user_id=user.id
    )
    data = await db.all(query)
    results = [dict(row) for row in data]
    return BoardListResponseModel(results=results)


@router.get("/{board_uuid}/")
async def board_detail(board_uuid: UUID, __=Depends(has_common_board_access)):

    query = BoardWithColumnsQueryFilter.base_query()
    results = await db.all(query)
    print(results)
    data = [dict(row) for row in results]
    # print(data)
    print(data)

    grouped = many_group_by(
        data=data, by=("board_uuid", "board_name"), to_field="columns"
    )
    # grouped = groupby(results, lambda __: __["board_uuid"])

    return grouped
