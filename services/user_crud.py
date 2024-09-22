from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user_models import User, Book, user_books_read
from schemas.user_schemas import UserCreate, BookCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Crud methods for users

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()



# Crud methods for books

def get_book_by_google_id(db: Session, google_id: str):
    return db.query(Book).filter(Book.google_id == google_id).first()

def mark_book_as_read(db: Session, *,user_id: int, book_id: int, interested: bool, comment: str):
    entry = user_books_read.insert().values(user_id=user_id, book_id=book_id, interested=interested, comment=comment)
    db.execute(entry)
    db.commit()

def create_book(db: Session, book: BookCreate):
    db_book = Book(
        google_id=book.google_id,
        title=book.title
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_read_books(db: Session, user_id: int):
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