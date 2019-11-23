from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
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
