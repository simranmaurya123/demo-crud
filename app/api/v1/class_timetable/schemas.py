from typing import Optional
from pydantic import BaseModel
from datetime import time, datetime


class ClassTimetableCreate(BaseModel):
    class_id: int
    subject_id: int
    teacher_id: int
    day_of_week: str  # "Monday", "Tuesday", etc.
    start_time: time
    end_time: time
    room_number: Optional[str] = None


class ClassTimetableUpdate(BaseModel):
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None
    day_of_week: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_number: Optional[str] = None


class ClassTimetableRead(BaseModel):
    timetable_id: int
    class_id: int
    subject_id: int
    teacher_id: int
    day_of_week: str
    start_time: time
    end_time: time
    room_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
