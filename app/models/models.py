from datetime import datetime
from typing import List

from beanie import Document
from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field, HttpUrl


class BaseModel(PydanticBaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True


# TODO 나중에 Collection이 많아지고 비즈니스 로직이 복잡해지면, basemodel이랑 분리할것
class Users(BaseModel, Document):
    """유저 Collection"""

    social_id: str = Field(..., description="소셜 id")
    social_type: str = Field(..., description="소셜로그인 타입")
    nickname: str = Field(..., description="닉네임")
    profile: str = Field(description="프로필 이미지")
    email: str = Field(..., description="이메일 주소")
    is_deleted: int = Field(..., description="활성화 여부 - 0:비활성, 1:활성")
    is_admin: int = Field(..., description="관리자 여부 - 0:일반유저, 1:관리자")

    class Settings:
        collection = "users"


class EasterEggs(BaseModel, Document):
    user_id: str = Field(..., description="유저 id")
    egg_word: str = Field(..., description="이스터에그 단어")
    hint: str = Field(..., description="힌트")
    gif_url: HttpUrl = Field(..., description="GIF url")
    is_deleted: str = Field(..., description="삭제 여부 - 1:삭제")  # soft delete
    corrected_by: List[str] = Field(default=[], description="정답을 맞춘 유저")

    class Settings:
        collection = "easter_eggs"


class ReadBy(BaseModel):
    reader_id: str = Field(..., description="읽은 유저 id")
    read_at: datetime = Field(..., description="읽은 시간")


class Message(BaseModel, Document):
    sender_id: str = Field(..., description="메세지 보낸 사람")
    message: str = Field(..., description="메세지")
    last_message_time: datetime = Field(
        ..., description="메세지 보낸시간 - 마지막 메세지 시간"
    )  # index 걸을 예정
    last_message_text: str = Field(..., description="메세지 - 마지막으로 보낸 메세지")
    read_by: List[ReadBy] = Field(default=[], description="읽은사람과 시간")


class Chats(BaseModel, Document):
    room_id: str = Field(..., description="방번호")
    users: List[str] = Field(..., description="채팅방에 참여한 유저")
    messages: List[Message] = Field(default=[], description="메세지")
    room_link: str = Field(description="채팅방 링크")

    class Settings:
        collection = "chats"
