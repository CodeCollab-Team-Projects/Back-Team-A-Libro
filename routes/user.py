from auth import auth
from datetime import timedelta
from services import user_crud 
from sqlalchemy.orm import Session
from config.database import get_db
from model.user_models import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, HTTPException, status, Depends
from schemas.user_schemas import UserCreate, UserResponse, UserUpdate, UserRegister

user = APIRouter()

@user.post("/register", response_model=UserRegister)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")
    return user_crud.create_user(db=db, user=user)

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
        data={"sub": user.id}, expires_delta=access_token_expires
    )
    return {"msg": "Login successful", "user": user.username, "access_token": access_token}

@user.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(auth.get_current_user)):
    return user_crud.user_to_response(current_user)


@user.put("/me", response_model=UserResponse)
def update_user_profile(update: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(auth.get_current_user)):
    updated_user = user_crud.update_user_profile(db, current_user, update)
    return user_crud.user_to_response(updated_user)

