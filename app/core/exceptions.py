from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
    HTTP_403_FORBIDDEN,
)
from fastapi import HTTPException


class DBError(ValueError):
    def __init__(self, err_msg):
        self.msg = err_msg


class Http404(HTTPException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, status_code=HTTP_404_NOT_FOUND)


class Unauthorized(HTTPException):
    detail = "Not authenticated"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail: str = ""):
        detail = detail or self.detail
        super().__init__(
            detail=detail, status_code=HTTP_401_UNAUTHORIZED, headers=self.headers
        )


class Http422(HTTPException):
    detail = "Errors while validating data"

    def __init__(self, detail: dict = None):
        if detail is not None and "detail" in detail:
            detail = detail.pop("detail")
        super().__init__(
            status_code=HTTP_422_UNPROCESSABLE_ENTITY, detail=detail or self.detail
        )


class Http403(HTTPException):
    detail = "You don't have permission to perform this action"

    def __init__(self, detail: str = None):
        super().__init__(status_code=HTTP_403_FORBIDDEN, detail=detail or self.detail)
