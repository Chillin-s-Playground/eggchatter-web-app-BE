from typing import Optional

from beanie import Document
from pydantic import Field

from app.models.basemodel import BaseModel


class Users(BaseModel, Document):
    """유저 Collection"""

    social_id: str = Field(..., description="소셜 id")
    social_type: str = Field(..., description="소셜로그인 타입")
    nickname: Optional[str] = Field(None, description="닉네임")
    profile: Optional[str] = Field(None, description="프로필 이미지")
    email: str = Field(..., description="이메일 주소")
    is_deleted: int = Field(..., description="활성화 여부 - 0:비활성, 1:활성")
    is_admin: int = Field(..., description="관리자 여부 - 0:일반유저, 1:관리자")
    is_invited: int = Field(..., description="초대 여부 - 0:일반가입, 1:초대가입")

    class Settings:
        collection = "users"
