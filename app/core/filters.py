from abc import ABC, abstractmethod
from typing import Type

from pydantic import ValidationError, BaseModel
from sqlalchemy.sql import Select
from starlette.requests import Request

from app.core.exceptions import Http422


class AbstractBaseFilter(ABC):
    @classmethod
    @abstractmethod
    def base_query(cls, *args, **kwargs) -> Select:
        pass

    @classmethod
    def get_query_with_filters(
        cls, request: Request, model: Type["BaseModel"], **kwargs
    ) -> Select:
        """
        :param request:
        :param model: BaseModel model for validating data
        :param kwargs: params for base query
        :return: Query with filters
        """

        base_query = cls.base_query(**kwargs)
        filtered = cls.add_filters_from_request(request, model, base_query)
        return filtered

    @classmethod
    def add_filters_from_request(
        cls, request: Request, model: Type["BaseModel"], query: Select
    ) -> Select:
        try:
            query_params = model(**request.query_params)
        except ValidationError as e:
            raise Http422(e.errors())

        for k, v in reversed(list(query_params)):
            field = getattr(cls, k, None)
            if v is not None and field is not None:
                query = field(value=v, request=request, query=query)

        return query
