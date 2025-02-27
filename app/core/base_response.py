from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    """공통 response DTO"""

    status_code: int
    data: Any
    message: str = "success"
