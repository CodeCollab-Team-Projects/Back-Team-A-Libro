from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from config.database import get_db
from services.user_crud import create_user, get_user_by_username
from auth import auth
from datetime import timedelta
from schemas.user_schemas import UserCreate, User, UserResponse


user = APIRouter()



@user.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return create_user(db=db, user=user)



@user.post("/login")
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"msg": "Login successful", "user": user.username, "access_token": access_token}



@user.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return current_user