from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    id: int
    username:str

class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

