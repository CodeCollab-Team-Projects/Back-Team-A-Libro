from sqlalchemy import select, update
from sqlalchemy.orm import Session
from schemas.book_schemas import BookCreate, UpdateBookData
from model.user_models import Book, user_books_read

import uuid


def get_book_by_google_id(db: Session, google_id: str):
    return db.query(Book).filter(Book.google_id == google_id).first()

def mark_book_as_read(db: Session, *,user_id: str, book_id: str, interested: bool, comment: str):
    entry = user_books_read.insert().values(user_id=user_id, book_id=book_id, interested=interested, comment=comment)
    db.execute(entry)
    db.commit()

def create_book(db: Session, book: BookCreate):
    db_book = Book(
        id=str(uuid.uuid4()),
        google_id=book.google_id,
        title=book.title
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_read_books(db: Session, user_id: str):
    result = db.execute(
        select(
            Book.id.label('book_id'),
            Book.google_id,
            Book.title,
            user_books_read.c.interested,
            user_books_read.c.comment
        )
        .join(user_books_read, Book.id == user_books_read.c.book_id)
        .filter(user_books_read.c.user_id == user_id)).all()
    return result


def delete_book(db: Session, user_id: int, google_id: str):
    book = get_book_by_google_id(db, google_id)
    if not book:
        raise ValueError("El libro no se encontro.")

    entry = db.query(user_books_read).filter(
        user_books_read.c.user_id == user_id,
        user_books_read.c.book_id == book.id
    ).first()

    if not entry:
        raise ValueError("Este libro no se a marcado como leído.")

    db.execute(user_books_read.delete().where(
        user_books_read.c.user_id == user_id,
        user_books_read.c.book_id == book.id
    ))
    db.commit()
    return {"message": "Libro eliminado con exíto."}

def update_book(db: Session, user_id: str, book_id: str, update_data: UpdateBookData):
    user_book_entry = db.query(user_books_read).filter(
        user_books_read.c.user_id == user_id,
        user_books_read.c.book_id == book_id
    ).first()

    if not user_book_entry:
        raise ValueError("No marcaste este libro como leído.")
    
    update_values = {}
    if update_data.interested is not None:
        update_values['interested'] = update_data.interested
    if update_data.comment is not None:
        update_values['comment'] = update_data.comment

    if update_values:
        stmt = (
            update(user_books_read).
            where(
                user_books_read.c.user_id == user_id,
                user_books_read.c.book_id == book_id
            ).
            values(**update_values)
        )
        db.execute(stmt)
        db.commit()

    return {"message": "Libro actualizado exitosamente", "book_id": book_id}