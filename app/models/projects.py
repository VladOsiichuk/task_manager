from pydantic import BaseModel, BaseConfig
from typing import List

# BaseConfig.use_orm = True
BaseConfig.orm_mode = True

class ProjectPydantic(BaseModel):
    id: int
    name: str


class ProjectInResponse(BaseModel):
    project: ProjectPydantic


class ProjectList(BaseModel):
    results: List[ProjectPydantic] = []
    # orm_mode=  True

# ProjectList.from_orm = True