from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# User Schemas

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


# Book Schemas

class Book(BaseModel):
    id: str
    title: str
    authors: str
    description: str
    average_rating: float

    class Config:
        orm_mode = True

class BookResponse(BaseModel):
    id: str
    title: str
    subtitle: Optional[str] = None
    authors: List[str]
    description: str
    categories: List[str]
    average_rating: float
    image_link: Optional[str] = None
    language: Optional[str] = None
    page_count: Optional[int] = None
    published_date: Optional[str] = None
    isbn: Optional[str] = None

    class Config:
        orm_mode = True
# Esquema para libros leídos (con campos de la tabla intermedia)
class ReadBook(BaseModel):
    book_id: int
    google_id: str
    title: str
    description: Optional[str] = None
    interested: bool
    comment: Optional[str] = None

    class Config:
        orm_mode = True

# Esquema para crear libros
class BookCreate(BaseModel):
    google_id: str
    title: str

    class Config:
        orm_mode = True