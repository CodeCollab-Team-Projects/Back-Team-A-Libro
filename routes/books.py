import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from config.database import get_db
from auth import auth
from schemas.user_schemas import Book, User, BookCreate, ReadBook, BookResponse
from services.user_crud import mark_book_as_read, get_read_books
from services import api_google
from typing import List, Optional

book = APIRouter()

@book.get("/search", response_model=List[BookResponse])
def get_books(query: Optional[str] = Query(None, description="Buscar libros por título o autor")):
    books_data = api_google.fetch_books_from_google(query)
    books = api_google.process_books_data(books_data)

    return books

# Marcar un libro como leído
@book.post("/favorite/{google_id}/mark_read")
def mark_book(google_id: str, interested: bool, comment: str, current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    book = api_google.get_or_create_book(db, google_id)
    mark_book_as_read(db, user_id=current_user.id, book_id=book.id, interested=interested, comment=comment)
    return {"message": "Libro marcado como leído", "book_id": book.id}


@book.get("/me/read_books", response_model=List[ReadBook])
def get_read_books_user(current_user: User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    books = get_read_books(db, user_id=current_user.id)
    return books
