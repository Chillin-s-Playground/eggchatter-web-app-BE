from datetime import datetime

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        arbitrary_types_allowed = True
