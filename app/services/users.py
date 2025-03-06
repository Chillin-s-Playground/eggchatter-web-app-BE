from sqlalchemy import update
from sqlalchemy.exc import DataError, SQLAlchemyError

from app.core.exceptions import SQLDataErrorException
from app.models.users import Users
from app.schemas.users import CreateProfileDTO


class UserService:
    def __init__(self, db=None):
        self.db = db

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
