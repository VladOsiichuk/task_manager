from typing import Dict, List

from fastapi import HTTPException
from pydantic import BaseModel
from app.core.exceptions import DBError


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


class ExceptionModel(BaseModel):
    detail: str
