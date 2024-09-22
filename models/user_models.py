from config.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey, Text, Table


user_books_read = Table(
    'user_books_read',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('interested', Boolean, default=False),
    Column('comment', String(255))
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))

    books_read = relationship('Book', secondary=user_books_read, back_populates="users_read")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    google_id = Column(String(255), unique=True, index=True) 
    title = Column(String(255), index=True)

    users_read = relationship("User", secondary=user_books_read, back_populates="books_read")
    

