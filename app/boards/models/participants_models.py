from typing import Union

from pydantic import UUID4, EmailStr, validator
from sqlalchemy import and_

from app.core.exceptions import Http404
from app.core.pydantic.models import ProjectPydanticBase
from app.core.pydantic.validators import primary_key_exists
from app.crud.user_in_board_queries import join_user_and_board_query
from app.db.models import Board, db, UserOnBoard, User


class ParticipantRemoveRequestModel(ProjectPydanticBase):
    user_uuid: UUID4

    async def run_model_validation(self, errors, board_uuid):
        query = join_user_and_board_query(
            board_uuid=board_uuid, user_uuid=self.user_uuid
        )
        results = await db.all(query)
        if not results:
            raise Http404
        results = [dict(row) for row in results]

        if results[0]["role"] == UserOnBoard.ADMIN:
            errors["detail"] = errors.get("detail") or []
            errors["detail"].append("You can't remove admin of board!")
        else:
            await UserOnBoard.delete.where(
                UserOnBoard.uuid == results[0]["user_in_board_uuid"]
            ).gino.status()


class ParticipantUpdateRoleRequestModel(ProjectPydanticBase):
    user_uuid: UUID4
    role: str = Union[UserOnBoard.MODERATOR, UserOnBoard.STAFF]

    async def run_model_validation(self, errors, board_uuid):
        query = join_user_and_board_query(
            board_uuid=board_uuid, user_uuid=self.user_uuid
        )
        results = await db.all(query)
        if not results:
            raise Http404
        results = [dict(row) for row in results]

        if results[0]["role"] == UserOnBoard.ADMIN:
            errors["detail"] = errors.get("detail") or []
            errors["detail"].append("You can't create admin!")
        else:
            await UserOnBoard.update.values(role=self.role).where(
                UserOnBoard.uuid == results[0]["user_in_board_uuid"]
            ).gino.status()


class ParticipantsUpdateRoleResponseModel(ProjectPydanticBase):
    role: str
    user_uuid: str


class ParticipantsAddRequestModel(ProjectPydanticBase):
    email: EmailStr
    role: str

    @validator("role")
    def is_allowed_role(cls, value: str) -> str:
        if value.upper() not in [UserOnBoard.MODERATOR, UserOnBoard.STAFF]:
            raise ValueError("Role {} does not exist".format(value))

        return value.upper()

    async def run_model_validation(self, errors, board: Board):
        user = self.user

        participant_exists = await UserOnBoard.query.where(
            and_(UserOnBoard.board_id == board.id, UserOnBoard.user_id == user.id)
        ).gino.first()
        if participant_exists:
            errors["email"] = errors.get("email", None) or []
            errors["email"].append("This user is already participant of the board")

    class Config:
        extra = "allow"
        allow_mutation = True
        db_validators = {"email": [primary_key_exists]}
        main_model = User


class ParticipantsAddResponseModel(ProjectPydanticBase):
    role: str
    email: str
