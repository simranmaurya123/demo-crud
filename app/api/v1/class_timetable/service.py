from typing import Dict, Any, List, Optional
from app.db.query_helpers import row_to_dict, rows_to_list


def create_class_timetable(
    db,
    class_id: int,
    subject_id: int,
    teacher_id: int,
    day_of_week: str,
    start_time,
    end_time,
    room_number: str = None,
) -> Dict[str, Any]:
    """Create a new class timetable entry"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO class_timetable (class_id, subject_id, teacher_id, day_of_week, start_time, end_time)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at
        """
        cursor.execute(query, (class_id, subject_id, teacher_id, day_of_week, start_time, end_time))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_class_timetables(db) -> List[Dict[str, Any]]:
    """Get all timetable entries"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at FROM class_timetable ORDER BY day_of_week, start_time"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_class_timetable(db, timetable_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific timetable entry by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at FROM class_timetable WHERE timetable_id = %s"
        cursor.execute(query, (timetable_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_class_timetable_by_class(db, class_id: int) -> List[Dict[str, Any]]:
    """Get all timetable entries for a specific class (entire week)"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at FROM class_timetable WHERE class_id = %s ORDER BY day_of_week, start_time"
        cursor.execute(query, (class_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_class_timetable_by_day(db, class_id: int, day_of_week: str) -> List[Dict[str, Any]]:
    """Get timetable entries for a class on a specific day"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at FROM class_timetable WHERE class_id = %s AND day_of_week = %s ORDER BY start_time"
        cursor.execute(query, (class_id, day_of_week))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def update_class_timetable(db, timetable_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Update a class timetable entry"""
    cursor = db.cursor()
    try:
        # Build dynamic update query
        updates = []
        values = []
        for key, value in kwargs.items():
            if value is not None and key in ['class_id', 'subject_id', 'teacher_id', 'day_of_week', 'start_time', 'end_time']:
                updates.append(f"{key} = %s")
                values.append(value)
        
        if not updates:
            return get_class_timetable(db, timetable_id)
        
        values.append(timetable_id)
        query = f"UPDATE class_timetable SET {', '.join(updates)} WHERE timetable_id = %s RETURNING timetable_id, class_id, subject_id, teacher_id, day_of_week, start_time, end_time, created_at, updated_at"
        cursor.execute(query, values)
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_class_timetable(db, timetable_id: int) -> Optional[Dict[str, Any]]:
    """Delete a class timetable entry"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM class_timetable WHERE timetable_id = %s RETURNING timetable_id"
        cursor.execute(query, (timetable_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
