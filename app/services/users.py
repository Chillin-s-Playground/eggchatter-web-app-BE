from beanie import PydanticObjectId
from beanie.odm.operators.update.general import Set
from fastapi import HTTPException

from app.models.users import Users
from app.schemas.users import Profile


class UserService:
    def __init__(self, db=None):
        self.db = db

    async def create_user_info(self, id=PydanticObjectId, profile=Profile):

        user = await Users.get(id)

        print("user", user)

        if user is None:
            raise HTTPException(status_code=404, detail="User not found.")

        try:
            await user.update(
                Set({Users.name: profile.name, Users.profile: profile.profile})
            )
            print("업데이트 잘됐어.")
            print("profile.name", profile.name)
            print("profile.name", profile.name)
        except Exception as e:
            print(str(e))
