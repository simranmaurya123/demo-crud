from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/student-timetable", tags=["student-timetable"])


@router.get("/student/{student_id}", response_model=list[schemas.StudentTimetableRead])
def get_student_timetable(
    student_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get student's class timetable - entire weekly schedule (requires authentication)"""
    return service.get_student_timetable(db, student_id)


@router.get("/student/{student_id}/day/{day_of_week}", response_model=list[schemas.StudentTimetableRead])
def get_student_timetable_by_day(
    student_id: int,
    day_of_week: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get student's schedule for a specific day (requires authentication)"""
    return service.get_student_timetable_by_day(db, student_id, day_of_week)



