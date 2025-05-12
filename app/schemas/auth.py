from pydantic import BaseModel, Field


class CommonHeader(BaseModel):
    access_token: str | None = Field(None, description="액세스 토큰")
    refresh_token: str | None = Field(None, description="액세스 리프레쉬 토큰")


class SignUpDTOModel(BaseModel):
    """회원가입, 로그인 DTO"""

    login_type: str = Field(..., description="로그인 유형 (KAKAO, EMAIL)")
    profile_image: str = Field(..., description="프로필 이미지")
    nickname: str = Field(..., description="유저 닉네임")
    social_id: str | None = Field(None, description="소셜로그인 시 id값")
    email: str | None = Field(
        None,
        description="이메일 주소 (이메일 로그인일 경우 필수)",
    )
    password: str | None = Field(
        None, description="비밀번호 (이메일 로그인일 경우 필수)"
    )


class SocialUserDtoModel(BaseModel):
    """소셜 로그인으로 가져오는 회원 정보"""

    social_id: str = Field(..., description="소셜 id")
    email: str = Field(..., description="이메일 주소")
    nickname: str | None = Field(None, description="유저 닉네임")
    profile_image: str | None = Field(None, description="프로필 이미지")
