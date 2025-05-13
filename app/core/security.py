from datetime import datetime, timedelta

import bcrypt
from jose import ExpiredSignatureError, jwt

from app.core.config import configs
from app.core.exceptions import RequestDataMissingException, TokenExpiredException

SECRET_KEY = configs.SECRET_KEY
ALGORITHM = configs.ALGORITHM
REFRESH_SECRET_KEY = configs.REFRESH_SECRET_KEY
ALGORITHM = configs.ALGORITHM


def verify_password(plain_pw: str, hashed_pw: str) -> bool:
    """비밀번호 유효성 체크 메소드."""
    return bcrypt.checkpw(plain_pw.encode("utf-8"), hashed_pw.encode("utf-8"))


def create_jwt_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    """access_token 생성 메소드."""

    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_jwt_refresh_token(data, expires_delta: timedelta = timedelta(hours=6)):
    """refresh_token 생성 메소드."""

    to_encode = data.copy()
    to_encode["exp"] = datetime.now() + expires_delta
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_payload(access_token: str, refresh_token: str):
    """JWT를 디코딩하여 user_id 반환, 필요한 경우 토큰 갱신"""
    if not access_token or not refresh_token:
        raise RequestDataMissingException(detail="토큰이 필요합니다.")

    def extract_user_id(token: str, secret: str) -> int:
        payload = jwt.decode(token, secret, algorithms=ALGORITHM)
        return int(payload.get("sub"))

    try:
        user_id = extract_user_id(access_token, SECRET_KEY)
        return {"user_id": user_id}

    except ExpiredSignatureError:
        # access_token 만료 → refresh_token 확인
        try:
            user_id = extract_user_id(refresh_token, REFRESH_SECRET_KEY)
            data = {"sub": user_id}

            new_access_token = create_jwt_access_token(data=data)
            new_refresh_token = create_jwt_refresh_token(data=data)

            return {
                "user_id": user_id,
                "token": {
                    **new_access_token,
                    **new_refresh_token,
                },
            }

        except ExpiredSignatureError:
            # refresh_token도 만료됐을 경우 raise exception
            raise TokenExpiredException() from None
