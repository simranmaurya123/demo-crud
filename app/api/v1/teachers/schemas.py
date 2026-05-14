from pydantic import BaseModel, EmailStr


class TeacherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class TeacherUpdate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    age: int


class TeacherRead(BaseModel):
    teacher_id: int
    first_name: str
    last_name: str
    email: EmailStr
    age: int

    class Config:
        from_attributes = True
