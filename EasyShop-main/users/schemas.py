from pydantic import BaseModel
from typing import Optional


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    is_superuser: Optional[int]  = None

class LoginSchema(BaseModel):
    username: str
    password: str

class GetSchema(BaseModel):
    user_id: int # Super user idsini kiriting
    id: int