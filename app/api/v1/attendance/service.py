import logging
from datetime import date
from typing import Dict, Any, List, Optional

from app.db.query_helpers import row_to_dict, rows_to_list
from . import schemas

logger = logging.getLogger(__name__)


def create_attendance(db, attendance: schemas.AttendanceCreate) -> Dict[str, Any]:
    """Create a new attendance record"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO attendance (student_id, teacher_id, date, status, remarks)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING attendance_id, student_id, teacher_id, date, status, remarks, created_at
        """
        cursor.execute(query, (attendance.student_id, attendance.teacher_id, attendance.date, attendance.status, attendance.remarks))
        result = cursor.fetchone()
        db.commit()
        logger.info(f"Attendance created for student {attendance.student_id} on {attendance.date}")
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_attendance_by_id(db, attendance_id: int) -> Optional[Dict[str, Any]]:
    """Get attendance record by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT attendance_id, student_id, teacher_id, date, status, remarks, created_at FROM attendance WHERE attendance_id = %s"
        cursor.execute(query, (attendance_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_attendance_by_student_and_date(
    db, student_id: int, attendance_date: date
) -> Optional[Dict[str, Any]]:
    """Get attendance record for a specific student on a specific date"""
    cursor = db.cursor()
    try:
        query = "SELECT attendance_id, student_id, teacher_id, date, status, remarks, created_at FROM attendance WHERE student_id = %s AND date = %s"
        cursor.execute(query, (student_id, attendance_date))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_student_attendance_history(db, student_id: int) -> List[Dict[str, Any]]:
    """Get all attendance records for a student"""
    cursor = db.cursor()
    try:
        query = "SELECT attendance_id, student_id, teacher_id, date, status, remarks, created_at FROM attendance WHERE student_id = %s ORDER BY date DESC"
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_attendance_by_date(db, attendance_date: date) -> List[Dict[str, Any]]:
    """Get all attendance records for a specific date"""
    cursor = db.cursor()
    try:
        query = "SELECT attendance_id, student_id, teacher_id, date, status, remarks, created_at FROM attendance WHERE date = %s"
        cursor.execute(query, (attendance_date,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_attendance_by_teacher(db, teacher_id: int) -> List[Dict[str, Any]]:
    """Get all attendance records created by a specific teacher"""
    cursor = db.cursor()
    try:
        query = "SELECT attendance_id, student_id, teacher_id, date, status, remarks, created_at FROM attendance WHERE teacher_id = %s ORDER BY date DESC"
        cursor.execute(query, (teacher_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def update_attendance(
    db, attendance_id: int, attendance_update: schemas.AttendanceUpdate
) -> Optional[Dict[str, Any]]:
    """Update an attendance record"""
    cursor = db.cursor()
    try:
        db_attendance = get_attendance_by_id(db, attendance_id)
        if not db_attendance:
            return None
        
        updates = []
        values = []
        
        if attendance_update.status:
            updates.append("status = %s")
            values.append(attendance_update.status)
        if attendance_update.remarks is not None:
            updates.append("remarks = %s")
            values.append(attendance_update.remarks)
        
        if not updates:
            return db_attendance
        
        values.append(attendance_id)
        query = f"UPDATE attendance SET {', '.join(updates)} WHERE attendance_id = %s RETURNING attendance_id, student_id, teacher_id, date, status, remarks, created_at"
        cursor.execute(query, values)
        result = cursor.fetchone()
        db.commit()
        logger.info(f"Attendance record {attendance_id} updated")
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_attendance(db, attendance_id: int) -> bool:
    """Delete an attendance record"""
    cursor = db.cursor()
    try:
        db_attendance = get_attendance_by_id(db, attendance_id)
        if not db_attendance:
            return False
        
        query = "DELETE FROM attendance WHERE attendance_id = %s"
        cursor.execute(query, (attendance_id,))
        db.commit()
        logger.info(f"Attendance record {attendance_id} deleted")
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_student_attendance_report(db, student_id: int) -> Optional[Dict[str, Any]]:
    """Generate attendance report for a student"""
    cursor = db.cursor()
    try:
        # Get student info
        student_query = "SELECT first_name, last_name FROM students WHERE student_id = %s"
        cursor.execute(student_query, (student_id,))
        student_result = cursor.fetchone()
        
        if not student_result:
            return None
        
        # Get attendance records
        attendance_records = get_student_attendance_history(db, student_id)
        
        total_days = len(attendance_records)
        present_days = len([a for a in attendance_records if a.get('status', '').lower() == "present"])
        absent_days = len([a for a in attendance_records if a.get('status', '').lower() == "absent"])
        
        attendance_percentage = (
            (present_days / total_days * 100) if total_days > 0 else 0
        )
        
        return {
            "student_id": student_id,
            "first_name": student_result[0],
            "last_name": student_result[1],
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "attendance_percentage": round(attendance_percentage, 2),
        }
    finally:
        cursor.close()


