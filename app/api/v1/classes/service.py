from typing import Optional, Dict, Any, List
from app.db.query_helpers import row_to_dict, rows_to_list


# ========== CLASS OPERATIONS ==========

def create_class(db, class_name: str, grade_level: int, section: str = None, room_number: str = None) -> Dict[str, Any]:
    """Create a new class"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO classes (class_name, grade_level, section, room_number)
        VALUES (%s, %s, %s, %s)
        RETURNING class_id, class_name, grade_level, section, room_number, created_at, updated_at
        """
        cursor.execute(query, (class_name, grade_level, section, room_number))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_classes(db) -> List[Dict[str, Any]]:
    """Get all classes"""
    cursor = db.cursor()
    try:
        query = "SELECT class_id, class_name, grade_level, section, room_number, created_at, updated_at FROM classes ORDER BY class_id"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_class(db, class_id: int) -> Optional[Dict[str, Any]]:
    """Get a specific class by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT class_id, class_name, grade_level, section, room_number, created_at, updated_at FROM classes WHERE class_id = %s"
        cursor.execute(query, (class_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def update_class(db, class_id: int, **kwargs) -> Optional[Dict[str, Any]]:
    """Update a class"""
    cursor = db.cursor()
    try:
        # Build dynamic update query
        updates = []
        values = []
        for key, value in kwargs.items():
            if value is not None and key in ['class_name', 'grade_level', 'section', 'room_number']:
                updates.append(f"{key} = %s")
                values.append(value)
        
        if not updates:
            return get_class(db, class_id)
        
        values.append(class_id)
        query = f"UPDATE classes SET {', '.join(updates)} WHERE class_id = %s RETURNING class_id, class_name, grade_level, section, room_number, created_at, updated_at"
        cursor.execute(query, values)
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_class(db, class_id: int) -> Optional[Dict[str, Any]]:
    """Delete a class"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM classes WHERE class_id = %s RETURNING class_id"
        cursor.execute(query, (class_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


# ========== STUDENT ENROLLMENT OPERATIONS ==========

def enroll_student(db, student_id: int, class_id: int) -> Dict[str, Any]:
    """Enroll a student in a class"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO student_timetable (student_id, class_id)
        VALUES (%s, %s)
        RETURNING timetable_id, student_id, class_id, created_at, updated_at
        """
        cursor.execute(query, (student_id, class_id))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_student_class(db, student_id: int) -> Optional[Dict[str, Any]]:
    """Get the class a student is enrolled in"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, student_id, class_id, created_at, updated_at FROM student_timetable WHERE student_id = %s LIMIT 1"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_class_students(db, class_id: int) -> List[Dict[str, Any]]:
    """Get all students in a class"""
    cursor = db.cursor()
    try:
        query = "SELECT timetable_id, student_id, class_id, created_at, updated_at FROM student_timetable WHERE class_id = %s"
        cursor.execute(query, (class_id,))
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def remove_student_enrollment(db, enrollment_id: int) -> Optional[Dict[str, Any]]:
    """Remove a student from a class"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM student_timetable WHERE timetable_id = %s RETURNING timetable_id"
        cursor.execute(query, (enrollment_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
