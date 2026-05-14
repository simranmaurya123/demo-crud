from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=schemas.StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(
    student: schemas.StudentCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new student (requires authentication)"""
    return service.create_student(
        db, student.first_name, student.last_name, student.email, student.age
    )


@router.get("/", response_model=list[schemas.StudentRead])
def list_students(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all students (requires authentication)"""
    return service.get_students(db)


@router.get("/{student_id}", response_model=schemas.StudentRead)
def get_student(
    student_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a student by ID (requires authentication)"""
    db_student = service.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student


@router.put("/{student_id}", response_model=schemas.StudentRead)
def update_student(
    student_id: int,
    student: schemas.StudentUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a student (requires authentication)"""
    db_student = service.update_student(
        db, student_id, student.first_name, student.last_name, student.email, student.age
    )
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student


@router.delete("/{student_id}", response_model=schemas.StudentRead)
def delete_student(
    student_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a student (requires authentication)"""
    db_student = service.delete_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return db_student


