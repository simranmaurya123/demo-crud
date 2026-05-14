from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class StudentUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class StudentRead(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True
