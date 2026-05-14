import logging
from typing import Any
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_db, get_current_user
from . import schemas, service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/attendance", tags=["Attendance"])


@router.post(
    "/",
    response_model=schemas.AttendanceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Record Attendance",
    description="Create a new attendance record"
)
def record_attendance(
    attendance: schemas.AttendanceCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Record attendance for a student"""
    # Verify the current user is a teacher
    db_attendance = service.create_attendance(db, attendance)
    logger.info(f"Attendance recorded for student: {attendance.student_id}")
    return db_attendance


@router.get(
    "/{attendance_id}",
    response_model=schemas.AttendanceResponse,
    summary="Get Attendance Record",
    description="Get a specific attendance record by ID"
)
def get_attendance(
    attendance_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a specific attendance record"""
    db_attendance = service.get_attendance_by_id(db, attendance_id)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )
    return db_attendance


@router.get(
    "/student/{student_id}",
    response_model=list[schemas.AttendanceResponse],
    summary="Get Student Attendance History",
    description="Get all attendance records for a specific student"
)
def get_student_attendance(
    student_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get attendance history for a student"""
    attendance_records = service.get_student_attendance_history(db, student_id)
    return attendance_records


@router.get(
    "/date/{attendance_date}",
    response_model=list[schemas.AttendanceResponse],
    summary="Get Attendance by Date",
    description="Get all attendance records for a specific date"
)
def get_attendance_by_date(
    attendance_date: date,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all attendance for a specific date"""
    attendance_records = service.get_attendance_by_date(db, attendance_date)
    return attendance_records


@router.get(
    "/report/student/{student_id}",
    response_model=schemas.StudentAttendanceReport,
    summary="Get Student Attendance Report",
    description="Generate attendance report with statistics for a student"
)
def get_attendance_report(
    student_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get attendance report for a student"""
    report = service.get_student_attendance_report(db, student_id)
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return report


@router.put(
    "/{attendance_id}",
    response_model=schemas.AttendanceResponse,
    summary="Update Attendance",
    description="Update an existing attendance record"
)
def update_attendance(
    attendance_id: int,
    attendance_update: schemas.AttendanceUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update an attendance record"""
    db_attendance = service.update_attendance(db, attendance_id, attendance_update)
    if not db_attendance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )
    return db_attendance


@router.delete(
    "/{attendance_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete Attendance",
    description="Delete an attendance record"
)
def delete_attendance(
    attendance_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete an attendance record"""
    success = service.delete_attendance(db, attendance_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attendance record not found",
        )
    return None


