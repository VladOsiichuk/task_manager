import datetime
from typing import Optional, Any, Type, List, Dict, Union

from fastapi import HTTPException

from app.core.constants import MOBILE_PHONE_REGEX
from pydantic import BaseModel, EmailStr, BaseConfig, validator, UUID4, Schema, Field

from app.core.exceptions import DBError
from app.core.pydantic.models import ProjectPydanticBase
from app.core.pydantic.validators import validate_on_unique
from app.db.models import User


class UserBaseModel(ProjectPydanticBase):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: EmailStr

    class Config:
        orm_mode = True


class UserRegisterRequestModel(UserBaseModel):
    password_confirm: str
    password: str

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if values.get("password_confirm") != v:
            raise ValueError("Passwords don't match")
        return v

    @validator("email")
    def email_is_valid(cls, v, values, **kwargs):
        raise ValueError("Incorrect email")

    async def run_model_validation(self, raise_exception: bool = True):
        errors = await self.db_validate()
        if errors and raise_exception:
            raise HTTPException(400, detail=errors)
        return errors

    class Config:
        db_validators = {"email": [validate_on_unique]}
        main_model = User
        orm_mode = False


class UserRegisterResponseModel(UserBaseModel):
    uuid: str

    class Config:
        orm_mode = True


class UserLoginRequestModel(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = False


class UserLoginResponseModel(BaseModel):
    refresh: Dict[str, Union[str, datetime.timedelta]]
    access: Dict[str, Union[str, datetime.timedelta]]

    class Config:
        orm_mode = False


class UserAuthenticateRequestModel(BaseModel):
    token: str
