from datetime import datetime
from typing import List

from beanie import Document
from pydantic import Field

from app.models.basemodel import BaseModel


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
