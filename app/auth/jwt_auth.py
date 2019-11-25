from datetime import datetime
from typing import Dict, Any, Union

import jwt
from fastapi.security.utils import get_authorization_scheme_param
from jwt import PyJWTError
from starlette.requests import Request

from app.core.config import JWT_SETTINGS
from app.core.exceptions import Unauthorized
from app.db.models import User


class JWTAuthentication:

    pk = "id"

    def __init__(self):
        pass

    async def __call__(self, request: Request):
        authorization: str = request.headers.get("Authorization")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise Unauthorized("Token schema invalid!")

        data = await self.payload(param)
        return await self.get_user_or_error(data)

    async def token_pair_generate(self, data: dict) -> dict:

        access_token = await self.access_generate(data)
        refresh_token = await self.refresh_generate(data, access_token)

        return {
            "access": {
                "expire_in": JWT_SETTINGS["ACCESS_EXPIRE_IN"],
                "token": str(access_token),
            },
            "refresh": {
                "expire_in": JWT_SETTINGS["REFRESH_EXPIRE_IN"],
                "token": refresh_token,
            },
        }

    @classmethod
    async def payload(cls, token: str, verify: bool = False) -> dict:
        try:

            payload = jwt.decode(
                token,
                JWT_SETTINGS["SECRET_KEY"],
                algorithms=[JWT_SETTINGS["ALGORITHM"]],
                verify=verify,
            )

        except PyJWTError:
            raise Unauthorized(detail="Token is invalid or expired!")
        else:
            return payload

    @staticmethod
    async def refresh_generate(data: Dict[str, Any], access_token: str) -> str:
        user_data = data.copy()

        payload = {"user_data": user_data}
        expire = datetime.utcnow() + JWT_SETTINGS["REFRESH_EXPIRE_IN"]
        payload.update({"exp": expire, "access": access_token})
        encoded_jwt = jwt.encode(
            payload, JWT_SETTINGS["SECRET_KEY"], algorithm=JWT_SETTINGS["ALGORITHM"]
        )

        return encoded_jwt.decode()

    @staticmethod
    async def access_generate(data: dict) -> str:
        payload = data.copy()
        expire = datetime.utcnow() + JWT_SETTINGS["ACCESS_EXPIRE_IN"]
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(
            payload, JWT_SETTINGS["SECRET_KEY"], algorithm=JWT_SETTINGS["ALGORITHM"]
        )

        return encoded_jwt.decode()

    async def get_access_from_refresh(
        self, refresh_token: str
    ) -> Dict[str, Union[str, int]]:

        payload = await self.payload(refresh_token)

        if not payload.get("access"):
            raise Unauthorized("Access token is invalid!")

        new_access = await self.access_generate(payload["user_data"])
        return {"token": new_access, "expire_in": JWT_SETTINGS["ACCESS_EXPIRE_IN"]}

    async def get_user_or_error(self, data):
        user: User = await User.query.where(User.id == data.get(self.pk)).gino.first()
        if not user:
            raise Unauthorized("Token is incorrect!")
        return user


jwt_auth = JWTAuthentication()
