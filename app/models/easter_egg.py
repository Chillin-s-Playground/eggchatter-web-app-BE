from typing import List

from beanie import Document
from pydantic import Field, HttpUrl

from app.models.basemodel import BaseModel


class EasterEggs(BaseModel, Document):
    user_id: str = Field(..., description="유저 id")
    egg_word: str = Field(..., description="이스터에그 단어")
    hint: str = Field(..., description="힌트")
    gif_url: HttpUrl = Field(..., description="GIF url")
    is_deleted: str = Field(..., description="삭제 여부 - 1:삭제")  # soft delete
    corrected_by: List[str] = Field(default=[], description="정답을 맞춘 유저")

    class Settings:
        collection = "easter_eggs"
