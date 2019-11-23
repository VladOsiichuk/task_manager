import datetime
from typing import Optional, Any, Type, List, Dict, Union

from fastapi import HTTPException

from app.core.constants import MOBILE_PHONE_REGEX
from pydantic import BaseModel, EmailStr, BaseConfig, validator, UUID4, Schema

from app.core.exceptions import DBError
from app.core.pydantic.validators import validate_on_unique
from app.db.models import User


class ProjectPydanticBase(BaseModel):
    async def db_validate(self, raise_exception: bool = False) -> dict:
        """
        :param raise_exception: should exception be rised or none
        :return: dict of errors if any
        """

        model = self.__config__.main_model

        errors: Dict[str, List] = {}

        for field, validators in self.__config__.db_validators.items():
            value = getattr(self, field)

            for validate in validators:
                try:
                    self.__dict__[field] = await validate(model, field, value) or value
                except DBError as e:
                    if field not in errors:
                        errors[field] = list()
                    errors[field].append(e.msg)

        if raise_exception and errors:
            raise HTTPException(status_code=400, detail=errors)

        else:
            return errors


class UserBaseModel(ProjectPydanticBase):
    first_name: Optional[str] = ""
    last_name: Optional[str] = ""
    email: EmailStr
    mobile_phone: str = Schema(
        default="", max_length=15, min_length=4, regex=MOBILE_PHONE_REGEX
    )

    class Config:
        orm_mode = True
        db_validators = {
            "mobile_phone": [validate_on_unique],
            "email": [validate_on_unique],
        }
        main_model = User


class UserRegisterRequestModel(UserBaseModel):
    password_confirm: str
    password: str

    @validator("password")
    def passwords_match(cls, v, values, **kwargs):
        if values["password_confirm"] != v:
            raise ValueError("Passwords don't match")
        return v

    class Config:
        orm_mode = False


class UserRegisterResponseModel(UserBaseModel):
    uuid: Optional[UUID4] = ""

    @validator("uuid")
    def set_uuid_hex(cls, v):
        return v.hex

    class Config:
        use_orm = True


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
