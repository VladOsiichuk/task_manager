import asyncio
from typing import List, Dict, NamedTuple

from fastapi import APIRouter

from app.db.models import Project
from app.models.projects import ProjectList, ProjectPydantic

router = APIRouter()
#
# project_response_model = {
#     "results": List[ProjectPydantic],
#     # "count": int
# }


class NamedResponse(NamedTuple):
    results: List[ProjectPydantic]
    count: int = 0


@router.get("/projects", response_model=Dict[str, NamedResponse])
async def projects_list():
    projects = await Project.query.gino.all()
    print(projects)
    data = ProjectList(results=projects)
    return data


@router.post("/projects")
async def create_project():
    project = Project(name="First Project")
    await project.create()
