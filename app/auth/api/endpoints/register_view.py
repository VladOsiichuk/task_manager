from fastapi import APIRouter, Depends

from app.auth.jwt_auth import jwt_auth
from app.auth.models import (
    UserRegisterRequestModel,
    UserRegisterResponseModel,
    UserLoginRequestModel,
    UserLoginResponseModel,
)
from app.core.exceptions import Unauthorized
from app.db.models import User

router = APIRouter()


@router.post("/register/", response_model=UserRegisterResponseModel, status_code=201)
async def register(user: UserRegisterRequestModel):
    await user.db_validate(raise_exception=True)
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        mobile_phone=user.mobile_phone,
    )
    db_user.hash_password(user.password)
    await db_user.create()
    return UserRegisterResponseModel.from_orm(db_user)


@router.post("/login/", status_code=200, response_model=UserLoginResponseModel)
async def login(credentials: UserLoginRequestModel):

    user = await User.query.where(User.email == credentials.email).gino.first()
    if user is not None and user.password_is_valid(credentials.password):
        payload = {jwt_auth.pk: user.id}
        tokens = await jwt_auth.token_pair_generate(payload)
        return tokens

    raise Unauthorized


@router.post(
    "/authenticate/", status_code=200, response_model=UserRegisterResponseModel
)
async def authenticate(user: User = Depends(jwt_auth)):
    print(user)
    return UserRegisterResponseModel.from_orm(user)
