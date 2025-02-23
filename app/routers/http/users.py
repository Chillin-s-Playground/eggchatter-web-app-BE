from beanie import PydanticObjectId
from fastapi import APIRouter, Depends

from app.db.mongodb import get_db
from app.models.users import Users
from app.schemas.users import Profile, SignUp
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


@router.post("/create-test")
async def create_users(user: SignUp, db=Depends(get_db)):
    try:
        user_data = Users(**user.model_dump())
        await user_data.insert()
        return dict(result="success")
    except Exception as e:
        print(f"{str(e)}")
        return dict(result="fail")


@router.post("/info")
async def update_user_info(id: PydanticObjectId, profile: Profile, db=Depends(get_db)):
    """회원가입 후 프로필 및 닉네임 같은 유저정보 추가"""
    await UserService(db=db).create_user_info(id=id, profile=profile)
