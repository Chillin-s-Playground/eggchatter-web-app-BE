from sqlalchemy import update
from sqlalchemy.exc import DataError, SQLAlchemyError

from app.core.database import columns_to_dict
from app.core.exceptions import NotFoundError, SQLDataErrorException
from app.models.users import Users
from app.schemas.users import CreateProfileDTO


class UserService:
    def __init__(self, db=None):
        self.db = db

    async def get_user_id(self, social_id: str):
        """social_id값으로 user_id값 반환하는 메소드."""
        user_id = self.db.query(Users.id).filter(Users.social_id == social_id).scalar()
        if user_id is None:
            raise NotFoundError(detail=f"해당 사용자를 찾을 수 없습니다.")
        return user_id
