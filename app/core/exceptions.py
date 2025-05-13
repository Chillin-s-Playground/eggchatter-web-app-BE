from typing import Any, Dict, Optional

from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.base import BaseResponse
from app.core.error_code import ErrorCode


class CustomException(Exception):
    """커스텀 예외 기본 클래스"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_CODE = STATUS_CODE
    DEFAULT_MESSAGE = "오류가 발생했습니다."

    def __init__(
        self, detail: Optional[str] = None, headers: Optional[Dict[str, Any]] = None
    ):
        self.http_status_code = self.STATUS_CODE
        self.response = BaseResponse(
            status_code=self.ERROR_CODE, message=detail or self.DEFAULT_MESSAGE
        )
        self.headers = headers


class DuplicatedErrorException(CustomException):
    """중복된 데이터 오류"""

    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    ERROR_CODE = ErrorCode.DUPLICATED_ENTRY
    DEFAULT_MESSAGE = "이미 존재하는 데이터입니다."

    def __init__(self, detail: str | None = None):
        super().__init__(detail=f"{detail}" or self.DEFAULT_MESSAGE)


class UnknownErrorException(CustomException):
    """알 수 없는 서버오류"""

    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    ERROR_CODE = ErrorCode.UNKNOWN_ERROR
    DEFAULT_MESSAGE = "알 수 없는 오류가 발생했습니다."

    def __init__(self, detail: str | None = None):
        super().__init__(detail=f"{detail}" if detail else self.DEFAULT_MESSAGE)


class UnauthorizedErrorException(CustomException):
    """인증 실패 오류"""

    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    ERROR_CODE = ErrorCode.UNAUTHORIZED
    DEFAULT_MESSAGE = "회원 인증에 실패했습니다."

    def __init__(self, detail: str | None = None):
        super().__init__(detail=f"{detail}" if detail else self.DEFAULT_MESSAGE)


class RequestDataMissingException(HTTPException):
    """필수 요청 파라미터 누락 오류"""

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


async def exception_handler(_, exc: Exception):
    """CustomException 예외 발생 시 처리"""
    return JSONResponse(
        status_code=exc.http_status_code,
        content=exc.response.model_dump(),
        headers=exc.headers,
    )
