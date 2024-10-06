from typing import List, Optional
from config.database import get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, Query, HTTPException


from auth import auth
from services import api_google, book_crud
from schemas.user_schemas import UserBase
from schemas.book_schemas import BookResponse, ReadBook, UpdateBookData


book = APIRouter()


@book.get("/search", response_model=List[BookResponse])
def get_books(
    query: Optional[str] = Query(None, 
    description="Buscar libros por título o autor")):

    books_data = api_google.fetch_books_from_google(query)
    books = api_google.process_books_data(books_data)
    return books


@book.post("/favorite/{google_id}/mark_read")
def mark_book(
    google_id: str, 
              interested: bool, 
              comment: str, 
              rating: Optional[int] = Query(None, ge=1, le=5), 
              current_user: UserBase = Depends(auth.get_current_user), 
              db: Session = Depends(get_db)):
    
    book = api_google.get_or_create_book(db, google_id)
    response = book_crud.mark_book_as_read(
        db,
        user_id=current_user.id,
        book_id=book.id,
        interested=interested,
        comment=comment,
        rating=rating
    )
    return response


@book.get("/me/read_books", response_model=List[ReadBook])
def get_read_books_user(
    current_user: UserBase = Depends(auth.get_current_user), 
    db: Session = Depends(get_db)):

    books = book_crud.get_read_books(db, user_id=current_user.id)
    return books


@book.put("/books/favorite/{book_id}/update")
async def update_book(
    book_id: str, 
    update_data: UpdateBookData,
    db: Session = Depends(get_db),
    current_user: UserBase = Depends(auth.get_current_user)):
    
    try:
        updated_book = book_crud.update_book(
            db=db,
            user_id=current_user.id,
            book_id=book_id,
            update_data=update_data
        )
        return updated_book
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@book.delete("/favorite/{google_id}/delete")
def delete_book(
    google_id: str, 
    current_user: UserBase = Depends(auth.get_current_user), 
    db: Session = Depends(get_db)):
    try:
        message = book_crud.delete_book(db, current_user.id, google_id)
        return message
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
