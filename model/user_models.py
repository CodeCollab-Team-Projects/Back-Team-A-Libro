from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, ForeignKey, Table, Integer

import uuid

user_books_read = Table(
    'user_books_read',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('book_id', String(36), ForeignKey('books.id', ondelete="CASCADE"), primary_key=True),
    Column('interested', Boolean, default=False),
    Column('comment', String(255)),
    Column('rating', Integer)
)


user_favorite_categories = Table(
    'user_favorite_categories',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('category_id', String(36), ForeignKey('categories.id', ondelete="CASCADE"), primary_key=True)
)


user_favorite_authors = Table(
    'user_favorite_authors',
    Base.metadata,
    Column('user_id', String(36), ForeignKey('users.id', ondelete="CASCADE"), primary_key=True),
    Column('author_id', String(36), ForeignKey('authors.id', ondelete="CASCADE"), primary_key=True)
)


class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)

    country = Column(String(100), nullable=True)
    language = Column(String(50), nullable=True)

    books_read = relationship('Book', secondary=user_books_read, back_populates="users_read")
    favorite_categories = relationship('Category', secondary=user_favorite_categories, back_populates='users_favorites')
    favorite_authors = relationship('Author', secondary=user_favorite_authors, back_populates='users_favorites')


class Book(Base):
    __tablename__ = "books"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    google_id = Column(String(255), unique=True, index=True, nullable=False)
    title = Column(String(255), index=True, nullable=False)

    users_read = relationship("User", secondary=user_books_read, back_populates="books_read")


class Category(Base):
    __tablename__ = "categories"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(100), unique=True, nullable=False)

    users_favorites = relationship('User', secondary=user_favorite_categories, back_populates='favorite_categories')


class Author(Base):
    __tablename__ = "authors"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    name = Column(String(100), unique=True, nullable=False)

    users_favorites = relationship('User', secondary=user_favorite_authors, back_populates='favorite_authors')
