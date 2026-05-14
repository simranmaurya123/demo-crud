from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.post("/", response_model=schemas.TeacherRead, status_code=status.HTTP_201_CREATED)
def create_teacher(
    teacher: schemas.TeacherCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new teacher (requires authentication)"""
    return service.create_teacher(
        db, teacher.first_name, teacher.last_name, teacher.email, teacher.age
    )


@router.get("/", response_model=list[schemas.TeacherRead])
def list_teachers(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all teachers (requires authentication)"""
    return service.get_teachers(db)


@router.get("/{teacher_id}", response_model=schemas.TeacherRead)
def get_teacher(
    teacher_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a teacher by ID (requires authentication)"""
    db_teacher = service.get_teacher(db, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return db_teacher


@router.put("/{teacher_id}", response_model=schemas.TeacherRead)
def update_teacher(
    teacher_id: int,
    teacher: schemas.TeacherUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a teacher (requires authentication)"""
    db_teacher = service.update_teacher(
        db, teacher_id, teacher.first_name, teacher.last_name, teacher.email, teacher.age
    )
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return db_teacher


@router.delete("/{teacher_id}", response_model=schemas.TeacherRead)
def delete_teacher(
    teacher_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a teacher (requires authentication)"""
    db_teacher = service.delete_teacher(db, teacher_id)
    if not db_teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return db_teacher


