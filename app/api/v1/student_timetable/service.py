from typing import List, Dict, Any, Optional
from app.db.query_helpers import row_to_dict, rows_to_list


def get_student_timetable(db, student_id: int) -> List[Dict[str, Any]]:
    """Get student's class timetable - entire week schedule"""
    cursor = db.cursor()
    try:
        # Find which class the student is enrolled in
        enrollment_query = "SELECT class_id FROM student_timetable WHERE student_id = %s LIMIT 1"
        cursor.execute(enrollment_query, (student_id,))
        enrollment = cursor.fetchone()
        
        if not enrollment:
            return []
        
        class_id = enrollment[0]
        
        # Get the timetable for that class
        timetable_query = """
        SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at 
        FROM class_timetable 
        WHERE class_id = %s 
        ORDER BY day_of_week, start_time
        """
        cursor.execute(timetable_query, (class_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_student_timetable_by_day(db, student_id: int, day_of_week: str) -> List[Dict[str, Any]]:
    """Get student's schedule for a specific day"""
    cursor = db.cursor()
    try:
        # Find which class the student is enrolled in
        enrollment_query = "SELECT class_id FROM student_timetable WHERE student_id = %s LIMIT 1"
        cursor.execute(enrollment_query, (student_id,))
        enrollment = cursor.fetchone()
        
        if not enrollment:
            return []
        
        class_id = enrollment[0]
        
        # Get the timetable for that class on a specific day
        timetable_query = """
        SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at 
        FROM class_timetable 
        WHERE class_id = %s AND day_of_week = %s 
        ORDER BY start_time
        """
        cursor.execute(timetable_query, (class_id, day_of_week))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()

