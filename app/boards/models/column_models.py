from app.core.pydantic.models import ProjectPydanticBase
from app.db.models import BoardColumn, Board


class ColumnCreateRequestModel(ProjectPydanticBase):
    name: str


class ColumnCreateResponseModel(ProjectPydanticBase):
    uuid: str
    name: str
