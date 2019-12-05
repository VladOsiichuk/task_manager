from uuid import UUID

from fastapi import Depends, APIRouter
from starlette.requests import Request

from app.boards.models.boards_models import (
    BoardParticipantsListResponseModel,
    BoardParticipantsQueryParamsModel,
)
from app.boards.models.participants_models import (
    ParticipantRemoveRequestModel,
    ParticipantUpdateRoleRequestModel,
    ParticipantsUpdateRoleResponseModel,
    ParticipantsAddResponseModel,
    ParticipantsAddRequestModel,
)
from app.core.dependencies import has_common_board_access, is_board_moderator
from app.core.pydantic.models import ExceptionModel
from app.crud.board_queries import BoardParticipantsFilterQuery
from app.db.models import Board, UserOnBoard, db

router = APIRouter()


@router.post(
    "/{board_uuid}/participants/",
    status_code=201,
    response_model=ParticipantsAddResponseModel,
    responses={401: {"model": ExceptionModel}, 403: {"model": ExceptionModel}},
)
async def add_participants_to_board(
    board_uuid: UUID, data: ParticipantsAddRequestModel, __=Depends(is_board_moderator)
):
    board = await Board.query.where(Board.uuid == board_uuid).gino.first()
    await data.db_validate(board=board, raise_exception=True)
    new_participant = UserOnBoard(
        board_id=board.id, user_id=data.user.id, role=data.role
    )
    await new_participant.create()
    return ParticipantsAddResponseModel(email=data.user.email, role=data.role)


@router.get(
    "/{board_uuid}/participants/",
    response_model=BoardParticipantsListResponseModel,
    status_code=200,
    responses={403: {"model": ExceptionModel}, 401: {"model": ExceptionModel}},
)
async def participants_list(
    board_uuid: UUID, request: Request, __=Depends(has_common_board_access)
):
    query = BoardParticipantsFilterQuery.get_query_with_filters(
        request, model=BoardParticipantsQueryParamsModel, board_uuid=board_uuid
    )

    results = await db.all(query)
    data = [dict(row) for row in results]
    return BoardParticipantsListResponseModel(results=data)


@router.delete(
    "/{board_uuid}/participants/",
    status_code=204,
    responses={403: {"model": ExceptionModel}, 401: {"model": ExceptionModel}},
)
async def remove_participant(
    board_uuid: UUID,
    data: ParticipantRemoveRequestModel,
    __=Depends(is_board_moderator),
):
    await data.db_validate(board_uuid=board_uuid)
    return {"success": True}


@router.patch(
    "/{board_uuid}/participants/",
    status_code=200,
    response_model=ParticipantsUpdateRoleResponseModel,
    responses={403: {"model": ExceptionModel}, 401: {"model": ExceptionModel}},
)
async def change_user_role(
    board_uuid: UUID,
    data: ParticipantUpdateRoleRequestModel,
    __=Depends(is_board_moderator),
):
    await data.db_validate(board_uuid=board_uuid)
    return ParticipantsUpdateRoleResponseModel(
        role=data.role, user_uuid=data.user_uuid.hex
    )
