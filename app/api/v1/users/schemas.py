from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class UserUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class UserRead(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str
