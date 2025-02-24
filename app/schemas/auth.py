from pydantic import BaseModel, Field


class SignUp(BaseModel):
    social_id: str
    social_type: str
    email: str
    is_deleted: int
    is_admin: int
    is_invited: int
