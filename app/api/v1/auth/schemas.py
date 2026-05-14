from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int
    password: str


class UserLogin(BaseModel):
    username: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    subject: Optional[str] = None
