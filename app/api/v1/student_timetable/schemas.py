from typing import Optional
from pydantic import BaseModel
from datetime import time, datetime


class StudentTimetableRead(BaseModel):
    """Student's class timetable - shows their entire weekly schedule"""
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

