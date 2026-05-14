from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/classes", tags=["classes"])


# ========== CLASS ENDPOINTS ==========

@router.post("/", response_model=schemas.ClassRead, status_code=status.HTTP_201_CREATED)
def create_class(
    class_data: schemas.ClassCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new class (requires authentication)"""
    return service.create_class(
        db,
        class_data.class_name,
        class_data.grade_level,
        class_data.section,
        class_data.room_number,
    )


@router.get("/", response_model=list[schemas.ClassRead])
def list_classes(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all classes (requires authentication)"""
    return service.get_classes(db)


@router.get("/{class_id}", response_model=schemas.ClassRead)
def get_class(
    class_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a class by ID (requires authentication)"""
    db_class = service.get_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    return db_class


@router.put("/{class_id}", response_model=schemas.ClassRead)
def update_class(
    class_id: int,
    class_data: schemas.ClassUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a class (requires authentication)"""
    db_class = service.update_class(db, class_id, **class_data.dict(exclude_unset=True))
    if not db_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    return db_class


@router.delete("/{class_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_class(
    class_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a class (requires authentication)"""
    db_class = service.delete_class(db, class_id)
    if not db_class:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Class not found")
    return None


# ========== STUDENT ENROLLMENT ENDPOINTS ==========

@router.post("/enrollment/", response_model=schemas.StudentEnrollmentRead, status_code=status.HTTP_201_CREATED)
def enroll_student(
    enrollment: schemas.StudentEnrollmentCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Enroll a student in a class (requires authentication)"""
    return service.enroll_student(db, enrollment.student_id, enrollment.class_id)


@router.get("/{class_id}/students", response_model=list[schemas.StudentEnrollmentRead])
def get_class_students(
    class_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all students in a class (requires authentication)"""
    return service.get_class_students(db, class_id)


@router.delete("/enrollment/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_student_enrollment(
    enrollment_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Remove a student from a class (requires authentication)"""
    enrollment = service.remove_student_enrollment(db, enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Enrollment not found")
    return None


