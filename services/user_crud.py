import uuid
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from model.user_models import User, Category, Author
from schemas.user_schemas import UserCreate, UserUpdate, UserResponse


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_user(db: Session, user: UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = User(
        id=str(uuid.uuid4()), 
        username=user.username, 
        email=user.email, 
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: str):
    return db.query(User).filter(User.id == user_id).first()

def update_user_profile(db: Session, user: User, updates: UserUpdate):
    if updates.country is not None:
        user.country = updates.country
    if updates.language is not None:
        user.language = updates.language

    if updates.favorite_categories is not None:
        categories = []
        for cat_name in updates.favorite_categories:
            category = db.query(Category).filter(Category.name == cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.add(category)
                db.commit()
                db.refresh(category)
            categories.append(category)
        user.favorite_categories = categories

    if updates.favorite_authors is not None:
        authors = []
        for auth_name in updates.favorite_authors:
            author = db.query(Author).filter(Author.name == auth_name).first()
            if not author:
                author = Author(name=auth_name)
                db.add(author)
                db.commit()
                db.refresh(author)
            authors.append(author)
        user.favorite_authors = authors

    db.commit()
    db.refresh(user)
    return user

def user_to_response(user: User) -> UserResponse:
    favorite_categories = [category.name for category in user.favorite_categories]
    favorite_authors = [author.name for author in user.favorite_authors]

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        country=user.country,
        language=user.language,
        favorite_categories=favorite_categories,
        favorite_authors=favorite_authors
    )