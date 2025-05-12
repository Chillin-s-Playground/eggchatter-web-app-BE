from sqlite3 import IntegrityError

import bcrypt
from sqlalchemy import update
from sqlalchemy.exc import DataError, SQLAlchemyError

from app.core.database import columns_to_dict
from app.core.exceptions import (
    DuplicatedErrorException,
    NotFoundError,
    SQLDataErrorException,
    UnknownErrorException,
)
from app.models.users import Users
from app.schemas.users import CreateProfileDTO


class UserService:
    def __init__(self, db=None):
        self.db = db

    async def get_user_id(self, social_id: str):
        """social_id값으로 user_id값 반환하는 메소드."""
        user_id = self.db.query(Users.id).filter(Users.social_id == social_id).scalar()
        if user_id is None:
            raise NotFoundError(detail="해당 사용자를 찾을 수 없습니다.")
        return user_id

    def get_my_info(self, user_id: int):
        """user_id값으로 내 정보 가져오기"""
        user = (
            self.db.query(
                Users.email,
                Users.social_id,
                Users.login_type,
                Users.profile_image,
                Users.nickname,
            )
            .filter(Users.id == user_id)
            .first()
        )
        if user is None:
            raise NotFoundError(detail="해당 사용자를 찾을 수 없습니다.")
        return columns_to_dict(user)

    def create_profile(self, profile: CreateProfileDTO):
        """프로필 생성

        Args:
            profile (CreateProfileDTO): 닉네임과 유저의 프로필 이미지
        """
        try:
            stmt = (
                update(Users)
                .where(Users.id == profile.user_id)
                .values(nickname=profile.nickname, profile_image=profile.profile_image)
            )
            self.db.execute(stmt)
        except DataError as e:
            raise SQLDataErrorException(detail=f"입력하신 정보가 너무 깁니다.")
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"{str(e)}")
        return dict(nickname=profile.nickname, profile_image=profile.profile_image)
