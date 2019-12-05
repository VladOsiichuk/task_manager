import datetime
from typing import Optional, List

from fastapi import HTTPException
from pydantic import UUID4, validator, Field, ValidationError, EmailStr
from sqlalchemy import and_

from app.core.pydantic.validators import primary_key_exists, validate_on_unique
from app.core.pydantic.filter_models import LimitOffsetFilter
from app.core.pydantic.models import ProjectPydanticBase
from app.db.models import UserOnBoard, User, Board


class AuthorNestedModel(ProjectPydanticBase):
    email: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class BoardCreateRequestModel(ProjectPydanticBase):
    name: str


class BoardCreateResponseModel(ProjectPydanticBase):
    author: AuthorNestedModel
    name: str
    created_at: datetime.datetime
    uuid: Optional[UUID4] = ""

    @validator("uuid")
    def set_uuid_hex(cls, v):
        return v.hex

    class Config:
        orm_mode = True


class NestedBoardListResponseModel(ProjectPydanticBase):
    name: str
    uuid: str
    role: str
    created_at: datetime.datetime


class BoardListResponseModel(ProjectPydanticBase):
    results: List[NestedBoardListResponseModel]


class BoardQueryParamsModel(LimitOffsetFilter):
    my_boards: bool = None


class NestedBoardParticipantsListResponseModel(ProjectPydanticBase):
    role: str
    uuid: str
    email: str
    first_name: str = ""


class BoardParticipantsListResponseModel(ProjectPydanticBase):
    results: List[NestedBoardParticipantsListResponseModel]


class BoardParticipantsQueryParamsModel(ProjectPydanticBase):
    role: str = None
    uuid: str = None
