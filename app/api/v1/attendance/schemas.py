from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime


class AttendanceBase(BaseModel):
    student_id: int
    teacher_id: int
    date: date
    status: str  # "present" or "absent"
    remarks: Optional[str] = None


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceResponse(AttendanceBase):
    attendance_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class AttendanceUpdate(BaseModel):
    status: Optional[str] = None
    remarks: Optional[str] = None


class StudentAttendanceReport(BaseModel):
    student_id: int
    first_name: str
    last_name: str
    total_days: int
    present_days: int
    absent_days: int
    attendance_percentage: float
    
    class Config:
        from_attributes = True
