from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/teacher-timetable", tags=["teacher-timetable"])


@router.get("/teacher/{teacher_id}", response_model=list[schemas.TeacherTimetableRead])
def get_teacher_timetable(
    teacher_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get teacher's complete weekly schedule - all classes they teach (requires authentication)"""
    return service.get_teacher_timetables(db, teacher_id)


@router.get("/teacher/{teacher_id}/day/{day_of_week}", response_model=list[schemas.TeacherTimetableRead])
def get_teacher_timetable_by_day(
    teacher_id: int,
    day_of_week: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get teacher's schedule for a specific day (requires authentication)"""
    return service.get_teacher_timetable_by_day(db, teacher_id, day_of_week)


@router.get("/teacher/{teacher_id}/class/{class_id}", response_model=list[schemas.TeacherTimetableRead])
def get_teacher_timetable_by_class(
    teacher_id: int,
    class_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get teacher's schedule for a specific class (requires authentication)"""
    return service.get_teacher_timetable_by_class(db, teacher_id, class_id)



