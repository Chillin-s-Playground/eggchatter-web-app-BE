from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import relationship

from app.models.base import CommonFields


class ChatRooms(CommonFields):
    """채팅방 테이블"""

    __tablename__ = "chat_rooms"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    status = Column(
        String(4),
        nullable=False,
        comment="I : 초대는 했는데, 초대수락 안됨, O : 대화중, L: 대화 후 상대방이 나감.",
    )


class ChatRoomsUsers(CommonFields):
    """채팅방-유저 관계 테이블"""

    __tablename__ = "chat_rooms_users"

    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    chatroom_id = Column(BigInteger, ForeignKey("chat_rooms.id"), primary_key=True)


class Messages(CommonFields):
    """메세지 테이블"""

    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    chatroom_id = Column(BigInteger, ForeignKey("chatrooms.id"), nullable=False)
    sender_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)


class MessageReadStatus(CommonFields):
    """메세지읽음 상태 테이블"""

    __tablename__ = "message_read_status"

    message_id = Column(BigInteger, ForeignKey("messages.id"), primary_key=True)
    reader_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    read_at = Column(DateTime, nullable=False, default=func.current_timestamp())
