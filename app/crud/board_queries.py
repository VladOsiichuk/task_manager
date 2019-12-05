from typing import Type

import sqlalchemy as sa
from pydantic import BaseModel
from sqlalchemy import alias
from sqlalchemy.sql import Select
from starlette.requests import Request

from app.core.filters import AbstractBaseFilter
from app.db.models import Board, UserOnBoard, User, BoardColumn


class BoardWithColumnsQueryFilter:
    board_alias = alias(Board)
    columns_alias = alias(BoardColumn)

    @classmethod
    def base_query(cls):

        join = cls.board_alias.outerjoin(
            cls.columns_alias, cls.board_alias.c.id == cls.columns_alias.c.board_id
        )

        query = sa.select(
            [
                cls.board_alias.c.uuid.label("board_uuid"),
                cls.board_alias.c.name.label("board_name"),
                cls.columns_alias.c.name.label("column_name"),
                cls.columns_alias.c.uuid.label("column_uuid"),
            ]
        ).select_from(join)

        return query

    @classmethod
    def board_with_columns_query(cls, board_uuid):

        query = cls.base_query().where(cls.board_alias.c.uuid == board_uuid)

        return query


class BoardListFilterQuery(AbstractBaseFilter):
    user_alias = alias(User)
    board_alias = alias(Board)
    user_in_board_alias = alias(UserOnBoard)

    @classmethod
    def base_query(cls, user_id: int) -> Select:

        j = cls.board_alias.outerjoin(
            cls.user_in_board_alias,
            cls.board_alias.c.id == cls.user_in_board_alias.c.board_id,
        ).outerjoin(
            cls.user_alias, cls.user_in_board_alias.c.user_id == cls.user_alias.c.id
        )

        query = (
            sa.select(
                [
                    cls.board_alias,
                    cls.user_in_board_alias.c.role,
                    cls.user_alias.c.uuid.label("user_uuid"),
                ]
            )
            .select_from(j)
            .where(cls.user_in_board_alias.c.user_id == user_id)
            .distinct(cls.board_alias.c.id)
        )
        return query

    @classmethod
    def get_my_boards_filter(
        cls, request: Request, query: Select, value: bool = False
    ) -> Select:
        if value:
            query = query.where(cls.board_alias.c.author_id == request.user.id)
        else:
            query = query.where(cls.board_alias.c.author_id != request.user.id)
        return query

    @classmethod
    def get_query_with_filters(
        cls, request: Request, model: Type["BaseModel"], **kwargs
    ) -> Select:
        """
        :param request:
        :param model: BaseModel model for validating data
        :param kwargs: params for base query
        :return: Query with filters
        """

        base_query = cls.base_query(**kwargs)
        filtered = cls.add_filters_from_request(request, model, base_query)
        return filtered

    my_boards = get_my_boards_filter


class BoardParticipantsFilterQuery(AbstractBaseFilter):
    user_alias = alias(User, "users")
    user_in_board_alias = alias(UserOnBoard, "user_boards")
    board_alias = alias(Board)

    @classmethod
    def filter_user_uuid(cls, request: Request, query: Select, value: str):
        return query.where(cls.user_alias.c.uuid == value)

    @classmethod
    def filter_by_role(cls, request: Request, query: Select, value: str):
        return query.where(cls.user_in_board_alias.c.role == value)

    @classmethod
    def base_query(cls, board_uuid: str) -> Select:
        join = cls.user_in_board_alias.outerjoin(
            cls.board_alias, cls.user_in_board_alias.c.board_id == cls.board_alias.c.id
        ).outerjoin(
            cls.user_alias, cls.user_in_board_alias.c.user_id == cls.user_alias.c.id
        )

        query = (
            sa.select(
                [
                    cls.user_alias,
                    cls.board_alias.c.uuid.label("board_uuid"),
                    cls.user_in_board_alias.c.role,
                ]
            )
            .select_from(join)
            .where(cls.board_alias.c.uuid == board_uuid)
        )

        return query

    uuid = filter_user_uuid
    role = filter_by_role
