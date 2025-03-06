from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Integer, String, func

from app.models.base import CommonFields


class EasterEggs(CommonFields):
    """이스터에그 테이블"""

    __tablename__ = "easter_eggs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    trigger_word = Column(String(16), nullable=False)
    gif_url = Column(String(256), nullable=False)
    hint = Column(String(16), nullable=False)


class EasterEggHintHistory(CommonFields):
    """이스터에그 힌트 히스토리"""

    __tablename__ = "easter_egg_hint_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    chatroom_id = Column(BigInteger, ForeignKey("chatrooms.id"), nullable=False)
    easter_egg_id = Column(BigInteger, ForeignKey("easter_eggs.id"), nullable=False)
    is_used = Column(Integer, default=0)
    used_at = Column(DateTime, nullable=False, default=func.current_timestamp())


class EasterEggHistory(CommonFields):
    """이스터에그 히스토리 테이블"""

    __tablename__ = "easter_egg_history"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    trigger_user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    chatroom_id = Column(BigInteger, ForeignKey("chatrooms.id"), nullable=False)
    easter_egg_id = Column(BigInteger, ForeignKey("easter_eggs.id"), nullable=False)
    is_used = Column(Integer, default=0)
    triggered_at = Column(DateTime, nullable=False, default=func.current_timestamp())
