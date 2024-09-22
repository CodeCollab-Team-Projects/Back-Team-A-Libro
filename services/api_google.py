import requests
import random
from typing import Optional, List
from fastapi import HTTPException, Query
from sqlalchemy.orm import Session
from models.user_models import Book
from schemas.user_schemas import BookCreate, BookResponse
from services.user_crud import get_book_by_google_id, create_book


def get_or_create_book(db: Session, google_id: str) -> Book:
    book = get_book_by_google_id(db, google_id)

    if not book:
        url = f"https://www.googleapis.com/books/v1/volumes/{google_id}"
        response = requests.get(url)

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Libro no encontrado en Google Books API")

        book_data = response.json()
        book_info = book_data.get("volumeInfo", {})

        # Crear el objeto libro para la base de datos
        book = BookCreate(
            google_id=google_id,
            title=book_info.get("title", "Sin título")
        )

        # Guardar el libro en la base de datos
        book = create_book(db, book)

    return book


def fetch_books_from_google(query: Optional[str]) -> list:
    url = "https://www.googleapis.com/books/v1/volumes"
    params = {
        "q": query if query else "books",
        "maxResults": 20
    }
    response = requests.get(url, params=params)

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
            title=book_info.get("title", "Sin título"),
            subtitle=book_info.get("subtitle", "Sin subtítulo"),
            authors=(book_info.get("authors", [])),
            description=book_info.get("description", "Sin descripción"),
            categories=book_info.get("categories", []),
            average_rating=book_info.get("averageRating", 0.0),
            image_link=book_info.get("imageLinks", {}).get("thumbnail", None),
            language=book_info.get("language", "Desconocido"),
            page_count=book_info.get("pageCount", None),
            published_date=book_info.get("publishedDate", "Fecha desconocida"),
            isbn=None
        )

        for identifier in book_info.get("industryIdentifiers", []):
            if identifier.get("type") == "ISBN_13":
                book.isbn = identifier.get("identifier")

        books.append(book)

    return books

