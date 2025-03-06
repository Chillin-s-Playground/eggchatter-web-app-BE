from pydantic import BaseModel, Field


class CreateProfileDTO(BaseModel):
    # TODO user_id를 캐싱된 id값으로 처리할 수 있도록 변경
    user_id: int = Field(..., description="유저 id")
    profile_image: str = Field(..., description="프로필 이미지")
    nickname: str = Field(..., description="닉네임")
