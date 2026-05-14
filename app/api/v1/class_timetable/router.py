from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/class-timetable", tags=["class-timetable"])


@router.post("/", response_model=schemas.ClassTimetableRead, status_code=status.HTTP_201_CREATED)
def create_class_timetable(
    timetable: schemas.ClassTimetableCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new class timetable entry (requires authentication)"""
    return service.create_class_timetable(
        db,
        timetable.class_id,
        timetable.subject_id,
        timetable.teacher_id,
        timetable.day_of_week,
        timetable.start_time,
        timetable.end_time,
        timetable.room_number,
    )


@router.get("/", response_model=list[schemas.ClassTimetableRead])
def list_class_timetables(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all class timetable entries (requires authentication)"""
    return service.get_class_timetables(db)


@router.get("/{timetable_id}", response_model=schemas.ClassTimetableRead)
def get_class_timetable(
    timetable_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a class timetable entry by ID (requires authentication)"""
    db_timetable = service.get_class_timetable(db, timetable_id)
    if not db_timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
    return db_timetable


@router.get("/class/{class_id}", response_model=list[schemas.ClassTimetableRead])
def get_class_timetable_by_class(
    class_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all timetable entries for a class (entire week) (requires authentication)"""
    return service.get_class_timetable_by_class(db, class_id)


@router.get("/class/{class_id}/day/{day_of_week}", response_model=list[schemas.ClassTimetableRead])
def get_class_timetable_by_day(
    class_id: int,
    day_of_week: str,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get timetable entries for a class on a specific day (requires authentication)"""
    return service.get_class_timetable_by_day(db, class_id, day_of_week)


@router.put("/{timetable_id}", response_model=schemas.ClassTimetableRead)
def update_class_timetable(
    timetable_id: int,
    timetable: schemas.ClassTimetableUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a class timetable entry (requires authentication)"""
    db_timetable = service.update_class_timetable(db, timetable_id, **timetable.dict(exclude_unset=True))
    if not db_timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
    return db_timetable


@router.delete("/{timetable_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class_timetable(
    timetable_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a class timetable entry (requires authentication)"""
    db_timetable = service.delete_class_timetable(db, timetable_id)
    if not db_timetable:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Timetable entry not found")
    return None


