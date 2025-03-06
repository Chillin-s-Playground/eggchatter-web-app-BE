from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import CommonFields


class Users(CommonFields):
    """유저 테이블"""

    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(128), unique=True, nullable=False, comment="회원 이메일")
    social_id = Column(String(64), nullable=True, comment="소셜로그인 key")
    login_type = Column(
        String(40), nullable=False, comment="로그인 타입 (KAKAO, EMAIL, ...)"
    )
    password = Column(String(64), nullable=True, comment="비밀번호")
    profile_image = Column(String(64), nullable=True, comment="프로필 이미지")
    nickname = Column(String(40), nullable=False, comment="닉네임")
    is_admin = Column(Integer, default=0, nullable=False, comment="어드민 여부")
