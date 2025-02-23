from fastapi import APIRouter, Depends

from app.core.database import get_db
from app.schemas.auth import SignUp
from app.services.auth import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign_up")
async def create_user(req: SignUp, db=Depends(get_db)):
    """회원가입"""
    auth = AuthService(db=db)
    await auth.check_duplicate_user(req.email)
    return await auth.create_user(req=req)
