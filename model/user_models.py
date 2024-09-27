from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, ForeignKey, Table

import uuid

user_books_read = Table(
    'user_books_read',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id'), primary_key=True),
    Column('book_id', String(36), ForeignKey('books.id'), primary_key=True),
    Column('interested', Boolean, default=False),
    Column('comment', String(255))
)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

    books_read = relationship('Book', secondary=user_books_read, back_populates="users_read")


class Book(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    google_id = Column(String(255), unique=True, index=True) 
    title = Column(String(255), index=True)

    users_read = relationship("User", secondary=user_books_read, back_populates="books_read")
    

