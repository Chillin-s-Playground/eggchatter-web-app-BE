from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from pydantic import ValidationError


class RequestDataMissingException(HTTPException):
    """필수 요청 파라미터 누락 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        detail = "필수 요청 데이터가 누락되었습니다."
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class DuplicatedErrorException(HTTPException):
    """중복된 데이터 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class NotFoundError(HTTPException):
    """찾을 수 없는 데이터 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, headers)


class UnknownErrorException(HTTPException):
    """알 수 없는 서버오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, headers)


class ValidationErrorException(HTTPException):
    """Validation 오류"""

    def __init__(self, error: ValidationError):
        errors = error.errors()
        detail = errors
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail
        )


class SQLDataErrorException(HTTPException):
    """SQL 데이터 처리 관련 오류"""

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, headers)


class TokenExpiredException(HTTPException):
    """토큰 만료 오류"""

    def __init__(self, detail="토큰이 만료되었습니다.", headers=None):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, headers)
