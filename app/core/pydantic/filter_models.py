from pydantic import BaseModel


class LimitOffsetFilter(BaseModel):
    limit: int = 25
    offset: int = 0
    ordering: str = None
