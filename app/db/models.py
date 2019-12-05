import uuid

from gino import Gino
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.auth.utils import pwd_context

db = Gino()


class BaseModel(db.Model):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), default=func.now())
    uuid = Column(UUID, default=uuid.uuid4)
    is_active = Column(Boolean, default=True)

    __abstract__ = True


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String(128), default="")
    last_name = Column(String(128), default="")
    email = Column(String(256), default="", unique=True)
    password = Column(String(1024))

    def password_is_valid(self, plain_password: str) -> bool:
        """
        :param plain_password: password to check if correct
        """

        return pwd_context.verify(plain_password, self.password)

    def hash_password(self, plain_password: str):
        """
        """

        self.password = pwd_context.hash(plain_password)

    def __str__(self):
        return self.email


class Board(BaseModel):
    __tablename__ = "boards"

    name = Column(String(128))

    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User")


class BoardColumn(BaseModel):
    __tablename__ = "board_columns"
    name = Column(String(128))

    board_id = Column(Integer, ForeignKey(Board.id))
    board = relationship("Board", lazy="joined", foreign_keys="BoardColumn.board_id")


class UserOnBoard(BaseModel):
    __tablename__ = "user_boards"

    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"
    STAFF = "STAFF"

    user_id = Column(Integer, ForeignKey(User.id))
    user = relationship("User", lazy="joined", foreign_keys="UserOnBoard.user_id")

    role = Column(String(32), default=STAFF)

    board_id = Column(Integer, ForeignKey(Board.id))
    board = relationship("Board", lazy="joined", foreign_keys="UserOnBoard.board_id")


class Task(BaseModel):
    __tablename__ = "tasks"

    title = Column(String(64))
    description = Column(String(2048))
    deadline = Column(Date, default=None)

    author_id = Column(Integer, ForeignKey(User.id))
    author = relationship("User", lazy="joined", foreign_keys="Task.author_id")

    executor_id = Column(Integer, ForeignKey(User.id))
    executor = relationship("User", lazy="joined", foreign_keys="Task.author_id")
