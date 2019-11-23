import uuid

from gino import Gino
from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
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


class Project(BaseModel):
    __tablename__ = "projects"

    name = Column(String(128))


class Task(BaseModel):
    __tablename__ = "tasks"

    title = Column(String(64))
    description = Column(String(2048))
    deadline = Column(Date, default=None)
    executor = None


class User(BaseModel):
    __tablename__ = "users"

    first_name = Column(String(128), default="")
    last_name = Column(String(128), default="")
    email = Column(String(256), default="", unique=True)
    mobile_phone = Column(String(64), default="", unique=True)
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
