import datetime
from typing import Optional

from pydantic import UUID4, validator

from app.core.pydantic.models import ProjectPydanticBase


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
