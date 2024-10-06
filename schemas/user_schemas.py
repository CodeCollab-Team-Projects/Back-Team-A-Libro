from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=2, max_length=50)
    email: EmailStr

class UserRegister(UserBase):
    id: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    country: Optional[str] = None
    language: Optional[str] = None
    favorite_categories: List[str] = []
    favorite_authors: List[str] = []

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    country: Optional[str] = None
    language: Optional[str] = None
    favorite_categories: Optional[List[str]] = None  
    favorite_authors: Optional[List[str]] = None

class CategoryBase(BaseModel):
    name: str

class AuthorBase(BaseModel):
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
