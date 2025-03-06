from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String

from app.models.base import CommonFields


class Invitation(CommonFields):
    """초대 테이블"""

    __tablename__ = "invitations"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    link = Column(String(256), nullable=False)
    chatroom_id = Column(BigInteger, ForeignKey("chatrooms.id"), nullable=False)
    inviter_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    invitee_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    is_valid = Column(Integer, default=1)


class Friend(CommonFields):
    """친구 테이블"""

    __tablename__ = "friends"

    invitation_id = Column(BigInteger, ForeignKey("invitations.id"), primary_key=True)
    request_from = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    request_to = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    status = Column(
        String(4), nullable=False, comment="A : 친구, I : 친구삭제, B : 차단"
    )
