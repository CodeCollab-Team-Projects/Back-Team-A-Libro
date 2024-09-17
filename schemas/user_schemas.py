from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserDB(BaseModel):
    username: str
    email: EmailStr
    hashed_password: str

    class Config:
        orm_mode = True
