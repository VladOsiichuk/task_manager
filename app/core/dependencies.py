from starlette.requests import Request

from app.auth.jwt_auth import jwt_auth
from app.core.exceptions import Http403
from app.db.models import UserOnBoard, db
from app.crud.user_in_board_queries import join_user_and_board_query


async def has_common_board_access(request: Request):
    uuid = request.scope["path_params"]["board_uuid"]
    user = await jwt_auth(request)

    query = join_user_and_board_query(board_uuid=uuid, user_uuid=user.uuid.hex)
    results = await db.all(query)
    if not results:
        raise Http403
    return user


async def is_board_moderator(request: Request):
    uuid = request.scope["path_params"]["board_uuid"]
    user = await jwt_auth(request)

    query = join_user_and_board_query(board_uuid=uuid, user_uuid=user.uuid.hex)
    results = await db.all(query)
    if not results:
        raise Http403
    else:
        role = dict(results[0])["role"]
        if role not in [UserOnBoard.ADMIN, UserOnBoard.MODERATOR]:
            raise Http403

    return user
