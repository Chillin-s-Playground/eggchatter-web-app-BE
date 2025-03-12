from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.core.base import BaseResponse
from app.core.database import get_db
from app.core.security import create_jwt_access_token, create_jwt_refresh_token
from app.schemas.auth import AuthDtoModel, CommonHeader
from app.services.auth import AuthService
from app.services.users import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.get("/kakao/callback")
async def kakao_callback(req: Request):
    """카카오 서버 테스트용 redirect 경로"""
    code = req.query_params.get("code")
    auth = AuthService()
    res = await auth.kakao_auth_callback(code=code)
    print(res)
    return {"code": code}


@router.post("/signup", response_model=BaseResponse)
async def sign_up(
    req: AuthDtoModel,
    headers: Annotated[CommonHeader, Depends()],
    db=Depends(get_db),
) -> BaseResponse:
    """회원 가입 API"""
    auth = AuthService()

    # 로그인 타입에 따른 user_dat 분기처리
    if req.login_type == "KAKAO":
        social_user = await auth.get_kakao_user_info(access_token=headers.access_token)
        user_data = {**req.model_dump(), **social_user.model_dump()}

    # 신규유저 데이터 생성 후 user id값 반환
    user = UserService(db=db)
    user_id = await user.signup_new_user(user_data=user_data)

    # user id값으로 jwt token 생성
    data = {
        "sub": f"{user_id}",
    }
    access_token = create_jwt_access_token(data=data)
    refresh_token = create_jwt_refresh_token(data=data)

    token = {**access_token, **refresh_token}

    return BaseResponse(status_code=200, data=token)


@router.post("/signin")
async def signin(
    req: AuthDtoModel,
    headers: Annotated[CommonHeader, Depends()],
    db=Depends(get_db),
):
    auth = AuthService()
    if req.login_type == "KAKAO":
        social_user = await auth.get_kakao_user_info(access_token=headers.access_token)
        social_id = social_user.social_id

    user = UserService(db=db)
    user_id = await user.get_user_id(social_id=social_id)

    data = {
        "sub": f"{user_id}",
    }
    access_token = create_jwt_access_token(data=data)
    refresh_token = create_jwt_refresh_token(data=data)

    token = {**access_token, **refresh_token}

    return BaseResponse(status_code=200, data=token)
