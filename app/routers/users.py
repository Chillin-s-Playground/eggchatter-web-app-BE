from beanie import PydanticObjectId
from fastapi import APIRouter, Depends, status

from app.core.base_response import BaseResponse
from app.core.database import get_db
from app.models.users import Users
from app.schemas.users import CreateProfileDTO
from app.services.users import UserService

router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/profile")
async def create_my_profile(profile: CreateProfileDTO, db=Depends(get_db)):
    """프로필을 생성하는 API"""
    user = UserService(db=db).create_profile(profile=profile)

    return BaseResponse(
        status_code=status.HTTP_200_OK,
        data=user,
        message="프로필 생성 성공",
    )
