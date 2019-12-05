from typing import Dict, List, Optional, Any, Type
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel, validator
from app.core.exceptions import DBError, Http422


class ProjectPydanticBase(BaseModel):
    async def validate_from_config(self) -> dict:
        """
        :return: dict of errors if any
        """

        errors: Dict[str, List] = {}

        if not all(
            (
                hasattr(self.__config__, "main_model"),
                hasattr(self.__config__, "db_validators"),
            )
        ):
            return errors

        model = self.__config__.main_model

        for field, validators in self.__config__.db_validators.items():
            value = getattr(self, field)

            for validate in validators:
                try:
                    data = await validate(model, field, value)
                    if data is not None:
                        setattr(self, model.__name__.lower(), data)
                except DBError as e:
                    errors[field] = errors.get(field) or []
                    errors[field].append(e.msg)

        return errors

    async def db_validate(self, *args, raise_exception: bool = True, **kwargs) -> dict:
        errors = await self.validate_from_config()
        await self.run_model_validation(errors, *args, **kwargs)

        if errors and raise_exception:
            raise Http422(detail=errors)

        return errors

    async def run_model_validation(self, *args, **kwargs):
        pass

    class Config:
        orm_mode = True
        error_msg_templates = "{} {} {}"

    @classmethod
    def validate(cls: Type["Model"], value: Any):
        print("123")
        return super().validate(value)

    @validator("uuid", pre=True, check_fields=False)
    def set_uuid_hex(cls, v):
        if v and isinstance(v, UUID):
            return v.hex
        return v


class ExceptionModel(BaseModel):
    detail: Optional[str] = ""
