from sqlite3 import IntegrityError

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

    async def signup_new_user(self, user_data):
        """신규유저 생성 메소드."""
        try:
            user = Users(**user_data)
            self.db.add(user)
            self.db.flush()
            self.db.refresh(user)
            self.db.commit()
            return user.id
        except IntegrityError as e:
            self.db.rollback()
            error_msg = str(e).lower()
            if "email" in error_msg and (
                "unique" in error_msg or "duplicate" in error_msg
            ):
                raise DuplicatedErrorException(
                    detail="이미 사용 중인 이메일 주소입니다."
                ) from e
            else:
                raise DuplicatedErrorException(str(e)) from e
        except Exception as e:
            self.db.rollback()
            import logging

            logging.error(f"회원가입 중 오류 발생: {str(e)}")
            raise UnknownErrorException(detail=str(e)) from e

    async def get_user_id(self, social_id: str):
        """social_id값으로 user_id값 반환하는 메소드."""
        user_id = self.db.query(Users.id).filter(Users.social_id == social_id).scalar()
        if user_id is None:
            raise NotFoundError(detail="해당 사용자를 찾을 수 없습니다.")
        return user_id
