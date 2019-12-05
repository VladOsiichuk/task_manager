import sqlalchemy as sa
from sqlalchemy import alias, and_

from app.db.models import Board, User, UserOnBoard


def join_user_and_board_query(user_uuid, board_uuid):
    user_alias = alias(User)
    board_alias = alias(Board)
    user_on_board_alias = alias(UserOnBoard)

    join = user_on_board_alias.outerjoin(
        user_alias, user_on_board_alias.c.user_id == user_alias.c.id
    ).outerjoin(board_alias, user_on_board_alias.c.board_id == board_alias.c.id)

    query = (
        sa.select(
            [
                user_on_board_alias.c.role,
                user_on_board_alias.c.uuid.label("user_in_board_uuid"),
                user_alias.c.uuid.label("user_uuid"),
                board_alias.c.uuid.label("board_uuid"),
                board_alias.c.name,
                user_alias.c.email,
            ]
        )
        .select_from(join)
        .where(and_(board_alias.c.uuid == board_uuid, user_alias.c.uuid == user_uuid))
        .distinct(user_on_board_alias.c.id)
    )

    return query
