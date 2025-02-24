from pydantic import BaseModel, Field


class Profile(BaseModel):
    profile: str = Field(..., description="프로필 이미지")
    nickname: str = Field(..., description="닉네임")
