from typing import List, Dict, Any
from app.db.query_helpers import rows_to_list


def get_teacher_timetables(db, teacher_id: int) -> List[Dict[str, Any]]:
    """Get all classes a teacher teaches - entire week schedule"""
    cursor = db.cursor()
    try:
        query = """
        SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at 
        FROM class_timetable 
        WHERE teacher_id = %s 
        ORDER BY day_of_week, start_time
        """
        cursor.execute(query, (teacher_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_teacher_timetable_by_day(db, teacher_id: int, day_of_week: str) -> List[Dict[str, Any]]:
    """Get teacher's schedule for a specific day"""
    cursor = db.cursor()
    try:
        query = """
        SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at 
        FROM class_timetable 
        WHERE teacher_id = %s AND day_of_week = %s 
        ORDER BY start_time
        """
        cursor.execute(query, (teacher_id, day_of_week))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_teacher_timetable_by_class(db, teacher_id: int, class_id: int) -> List[Dict[str, Any]]:
    """Get teacher's schedule for a specific class"""
    cursor = db.cursor()
    try:
        query = """
        SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at 
        FROM class_timetable 
        WHERE teacher_id = %s AND class_id = %s 
        ORDER BY day_of_week, start_time
        """
        cursor.execute(query, (teacher_id, class_id))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()

