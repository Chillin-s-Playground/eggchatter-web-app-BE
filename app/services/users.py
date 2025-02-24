from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set

from app.core.exceptions import NotFoundError
from app.models.users import Users
from app.schemas.users import Profile


class UserService:
    def __init__(self, db=None):
        self.db = db

    async def update_user_profile(self, user_id: PydanticObjectId, req: Profile):
        """유저의 프로필 정보 업데이트"""
        user = await Users.get(user_id)
        if user is None:
            raise NotFoundError(
                detail=f"{user_id}에 해당하는 유저는 존재하지 않습니다."
            )
        await user.update(
            Set({Users.nickname: req.nickname, Users.profile: req.profile})
        )
