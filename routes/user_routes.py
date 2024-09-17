from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from config.database import get_conn, engine, Base
from services.user_crud import create_user, get_user_by_username
from schemas.user_schemas import UserCreate, UserDB, UserLogin
import bcrypt

user = APIRouter()

Base.metadata.create_all(bind=engine)

@user.post("/register", response_model=UserDB, tags = ["user"])
async def register(user: UserCreate, db: Session = Depends(get_conn)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    created_user = create_user(db, user)
    return created_user


@user.post("/login")
async def login(user: UserLogin, db: Session = Depends(get_conn)):
    db_user = get_user_by_username(db, user.username)
    if db_user is None or not bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"msg": "Login successful", "user": user.username}