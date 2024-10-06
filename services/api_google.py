import random
import requests
from fastapi import HTTPException
from typing import Optional, List
from sqlalchemy.orm import Session

from services import book_crud
from model.user_models import Book
from schemas.book_schemas import BookCreate, BookResponse

def get_or_create_book(db: Session, google_id: str) -> Book:
    book = book_crud.get_book_by_google_id(db, google_id)
    if book:
        return book

    url = f"https://www.googleapis.com/books/v1/volumes/{google_id}"
    response = requests.get(url)

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Límite de consultas a Google Books excedido")
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Libro no encontrado en Google Books API")

    book_data = response.json()
    book_info = book_data.get("volumeInfo", {})

    book = BookCreate(
        google_id=google_id,
        title=book_info.get("title", None), 
    )
    return book_crud.create_book(db, book)


def fetch_books_from_google(query: Optional[str]) -> list:
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query or "books",
        "maxResults": 20
    }
    response = requests.get(url, params=params)

    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="Límite de consultas a Google Books excedido")
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Error al obtener libros")

    return response.json().get("items", [])


def process_books_data(books_data: list) -> List[BookResponse]:
    random_books = random.sample(books_data, min(len(books_data), 20))

    books = []
    for item in random_books:
        book_info = item.get("volumeInfo", {})
        book = BookResponse(
            id=item["id"],
            title=book_info.get("title"),
            subtitle=book_info.get("subtitle"),
            authors=book_info.get("authors", []),
            description=book_info.get("description"),
            categories=book_info.get("categories", []),
            average_rating=book_info.get("averageRating", 0.0),
            image_link=book_info.get("imageLinks", {}).get("thumbnail"),
            language=book_info.get("language", "Desconocido"),
            page_count=book_info.get("pageCount"),
            published_date=book_info.get("publishedDate"),
            isbn=None
        )

        for identifier in book_info.get("industryIdentifiers", []):
            if identifier.get("type") == "ISBN_13":
                book.isbn = identifier.get("identifier")

        books.append(book)

    return books


