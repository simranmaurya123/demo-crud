from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ClassCreate(BaseModel):
    class_name: str
    section: Optional[str] = None
    grade_level: int
    room_number: Optional[str] = None


class ClassUpdate(BaseModel):
    class_name: Optional[str] = None
    section: Optional[str] = None
    grade_level: Optional[int] = None
    room_number: Optional[str] = None


class ClassRead(BaseModel):
    class_id: int
    class_name: str
    section: Optional[str] = None
    grade_level: int
    room_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class StudentEnrollmentCreate(BaseModel):
    student_id: int
    class_id: int


class StudentEnrollmentRead(BaseModel):
    enrollment_id: int
    student_id: int
    class_id: int
    enrollment_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True
