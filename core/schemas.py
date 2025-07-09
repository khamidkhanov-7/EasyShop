from pydantic import BaseModel, EmailStr, validator
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False


class UserLogin(BaseModel):
    username: str
    password: str

class UserGetRequest(BaseModel):
    current_user_id: int
    id: int

class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    owner: str

    @validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Narx manfiy bo'lishi mumkin emas")
        return v


class ProductUpdate(BaseModel):
    id: int
    owner_id: str
    name: Optional[str]
    description: Optional[str]
    price: Optional[int]


class ProductCreate(BaseModel):
    name: str
    description: str
    price: int
    owner: str

    @validator("price")
    def validate_price(cls, v):
        if v < 0:
            raise ValueError("Narx manfiy bo'lishi mumkin emas")
        return v


class ProductUpdate(BaseModel):
    id: int
    owner_id: str
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[int] = None

    @validator("price")
    def validate_price(cls, v):
        if v is not None and v < 0:
            raise ValueError("Narx manfiy bo'lishi mumkin emas")
        return v


class ProductRemove(BaseModel):
    owner_id: str
    id: int
