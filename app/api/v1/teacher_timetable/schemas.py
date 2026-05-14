from typing import Optional
from pydantic import BaseModel
from datetime import time, datetime


class TeacherTimetableRead(BaseModel):
    """Teacher's complete weekly schedule - all classes they teach"""
    timetable_id: int
    class_id: int
    subject_id: int
    day_of_week: str
    start_time: time
    end_time: time
    room_number: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

