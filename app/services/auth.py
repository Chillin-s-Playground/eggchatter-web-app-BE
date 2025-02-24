import traceback

from app.core.exceptions import DuplicatedError, UnknownError
from app.models.users import Users
from app.schemas.auth import SignUp


class AuthService:
    def __init__(self, db=None):
        self.db = db

    async def check_duplicate_user(self, email: str):
        """이메일 주소를 기반으로 중복회원가입 체크"""
        is_exist = await Users.find_one({"email": email})
        if is_exist:
            raise DuplicatedError(detail="이미 사용 중인 이메일 주소입니다.")

    async def create_user(self, req: SignUp):
        """새로운 유저 생성하는 메소드"""
        user_data = Users(**req.model_dump())
        try:
            result = await user_data.insert()
            return result
        except Exception:
            raise UnknownError(detail=f"{traceback.format_exc()[:1500]}")
