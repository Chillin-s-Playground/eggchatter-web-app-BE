import bcrypt
import httpx
from fastapi import Depends
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.session import Session

from app.core.config import configs
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

    async def is_registered_user(
        self, login_type: str, email: str, social_id: str | None = None
    ) -> bool:
        """회원가입된 유저여부를 반환하는 메소드."""

        if login_type == "EMAIL":
            user = (
                self.db.query(Users.id)
                .filter(Users.email == email, Users.login_type == login_type)
                .first()
            )
        else:
            user = self.db.query(Users.id).filter(Users.social_id == social_id).first()

        if user is None:
            return False
        return True

    async def is_existed_nickname(self, nickname: str) -> bool:
        """이미 존재하는 닉네임 여부 반환"""

        nickname = self.db.query(Users.id).filter(Users.nickname == nickname).first()
        return True if nickname else False

    async def signup_new_user(self, user_data):
        """신규유저 생성 메소드."""

        try:
            if user_data.get("login_type") == "EMAIL" and user_data.get("password"):
                hashed_pw = bcrypt.hashpw(
                    user_data.get("password").encode("utf-8"), bcrypt.gensalt()
                ).decode("utf-8")
                user_data["password"] = hashed_pw
            new_user = Users(**user_data)
            self.db.add(new_user)
        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e).lower()
            if "email" in error_msg and (
                "unique" in error_msg or "duplicate" in error_msg
            ):
                raise DuplicatedErrorException(
                    detail="이미 사용 중인 이메일 주소입니다."
                ) from e
            else:
                raise DuplicatedErrorException(str(e)) from e
        except SQLAlchemyError as e:
            self.db.rollback()
            raise UnknownErrorException(detail=str(e)) from e
        finally:
            self.db.commit()

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
            try:
                response = await client.post(
                    url=KAKAO_USER_ME_URL,
                    headers={
                        "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
                        "Authorization": f"Bearer {access_token}",
                    },
                    params={"property_keys[]": "kakao_account.email"},
                )
                response.raise_for_status()  # HTTP 오류 응답 확인
                user = response.json()
            except httpx.HTTPStatusError as e:
                raise UnknownErrorException(
                    detail=f"카카오 API 호출 중 오류 발생: {str(e)}"
                )
            except httpx.RequestError as e:
                raise UnknownErrorException(
                    detail=f"카카오 API 요청 중 오류 발생: {str(e)}"
                )

            try:
                social_id = user.get("id")
                if not social_id:
                    raise ValueError("카카오 소셜 ID를 찾을 수 없습니다")

                account = user.get("kakao_account", {})
                email = account.get("email")
                profile = account.get("profile", {})
                profile_image = profile.get("profile_image_url")
                nickname = profile.get("nickname")
            except (KeyError, TypeError) as e:
                raise UnknownErrorException(
                    detail=f"카카오 사용자 정보 파싱 중 오류 발생: {str(e)}"
                )

            return SocialUserDtoModel(
                social_id=f"{social_id}",
                email=email,
                nickname=nickname,
                profile_image=profile_image,
            )
