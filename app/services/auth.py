import httpx
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.core.config import configs
from app.core.database import columns_to_dict
from app.core.exceptions import (
    DuplicatedErrorException,
    NotFoundError,
    RequestDataMissingException,
    UnknownErrorException,
)
from app.core.security import decode_jwt_payload
from app.models.users import Users
from app.schemas.auth import CommonHeader, SocialUserDtoModel

KAKAO_AUTH_URL = "https://kauth.kakao.com/oauth/token"
KAKAO_USER_ME_URL = "https://kapi.kakao.com/v2/user/me"


def auth_check(headers: CommonHeader = Depends()):
    """API 회원 인증 검증 메소드. (주입해서 처리할 예정)"""
    access_token = headers.access_token
    refresh_token = headers.refresh_token

    if access_token is None or refresh_token is None:
        raise RequestDataMissingException()

    res = decode_jwt_payload(access_token=access_token, refresh_token=refresh_token)
    return res


class AuthService:
    def __init__(self, db: Session | None = None):
        self.db = db

        # res = decode_jwt_payload(access_token, refresh_token)

    async def kakao_auth_callback(self, code):
        """카카오 소셜로그인 callback 메소드."""
        async with httpx.AsyncClient() as client:
            res = (
                await client.post(
                    url=KAKAO_AUTH_URL,
                    data={
                        "grant_type": "authorization_code",
                        "client_id": configs.KAKAO_API_KEY,
                        "redirect_uri": configs.KAKAO_REDIRECT_URI,
                        "code": code,
                    },
                )
            ).json()

        return res

    async def get_kakao_user_info(self, access_token: str) -> SocialUserDtoModel:
        """카카오 회원정보 가져오는 메소드."""

        async with httpx.AsyncClient() as client:
            user = (
                await client.post(
                    url=KAKAO_USER_ME_URL,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                        "Authorization": f"Bearer {access_token}",
                    },
                    params={"property_keys[]": "kakao_account.email"},
                )
            ).json()

            social_id = user.get("id")
            account = user.get("kakao_account")
            email = account.get("email")
            profile = account.get("profile")
            profile_image = profile.get("profile_image_url")
            nickname = profile.get("nickname")

            return SocialUserDtoModel(
                social_id=f"{social_id}",
                email=email,
                nickname=nickname,
                profile_image=profile_image,
            )

    async def signup_new_user(self, user_data):
        """신규유저 생성 메소드."""
        try:
            user = Users(**user_data)
            self.db.add(user)
            self.db.flush()
            self.db.refresh(user)
            self.db.commit()

            return user.id
        except IntegrityError as e:
            if "for key 'users.email'" in str(e):
                raise DuplicatedErrorException(
                    detail="이미 사용 중인 이메일 주소입니다."
                ) from e
            else:
                raise DuplicatedErrorException(str(e)) from e
        except Exception as e:
            raise UnknownErrorException(detail=str(e)) from e
