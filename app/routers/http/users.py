from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.models.users import Users
from app.schemas.users import Profile
from app.services.users import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.get("/{id}")
async def get_users(id: PydanticObjectId, db=Depends(get_db)):
    """특정 유저 조회"""
    user = await Users.find_all().to_list()
    return user


@router.post("/info")
async def update_user_info(id: PydanticObjectId, profile: Profile, db=Depends(get_db)):
    """회원가입 후 프로필 및 닉네임 같은 유저정보 추가"""
    await UserService(db=db).create_user_info(id=id, profile=profile)
