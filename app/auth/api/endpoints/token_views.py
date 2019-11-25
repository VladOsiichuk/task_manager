from fastapi import APIRouter
from app.auth.models.auth_models import UserAuthenticateRequestModel
from app.auth.models.token_models import TokenRefreshResponseModel
from app.core.exceptions import Unauthorized
from app.core.pydantic.models import ExceptionModel
from app.auth.jwt_auth import jwt_auth


router = APIRouter()


@router.post(
    "/refresh/",
    status_code=200,
    response_model=TokenRefreshResponseModel,
    responses={401: {"model": ExceptionModel}},
)
async def token_refresh(data: UserAuthenticateRequestModel):
    refresh = data.token

    access_token_data = await jwt_auth.get_access_from_refresh(refresh)
    return TokenRefreshResponseModel(**access_token_data)


@router.post("/verify/", status_code=200)
async def token_verify(data: UserAuthenticateRequestModel):
    token = data.token
    is_valid = False
    try:
        payload = await jwt_auth.payload(token)
        if await jwt_auth.get_user_or_error(payload):
            is_valid = True
    except Unauthorized:
        pass
    response_data = {"is_valid": is_valid}
    return response_data
