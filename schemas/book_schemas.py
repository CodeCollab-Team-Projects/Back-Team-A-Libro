from pydantic import BaseModel
from typing import Optional, List


# Book Schemas

class Book(BaseModel):
    id: str
    title: str
    authors: str
    description: str
    average_rating: float

    class Config:
        from_attributes = True

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
        from_attributes = True

class ReadBook(BaseModel):
    book_id: str
    google_id: str
    title: str
    description: Optional[str] = None
    interested: bool
    comment: Optional[str] = None

    class Config:
        from_attributes = True


class BookCreate(BaseModel):
    google_id: str
    title: str

    class Config:
        from_attributes = True


class BookDetails(BaseModel):
    google_id: str
    title: str
    interested: bool
    comment: str

    class Config:
        from_attributes = True