from typing import Optional, Dict, Any, List
from app.db.query_helpers import row_to_dict, rows_to_list


def create_student(
    db,
    first_name: str,
    last_name: str,
    email: str,
    age: int,
    password_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new student"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO students (first_name, last_name, email, age, password_hash, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        RETURNING student_id, first_name, last_name, email, age, password_hash, is_active, created_at
        """
        cursor.execute(query, (first_name, last_name, email, age, password_hash))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_students(db) -> List[Dict[str, Any]]:
    """Get all students"""
    cursor = db.cursor()
    try:
        query = "SELECT student_id, first_name, last_name, email, age, is_active, created_at FROM students ORDER BY student_id"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_student(db, student_id: int) -> Optional[Dict[str, Any]]:
    """Get student by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT student_id, first_name, last_name, email, age, is_active, created_at FROM students WHERE student_id = %s"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_student_by_email(db, email: str) -> Optional[Dict[str, Any]]:
    """Get student by email"""
    cursor = db.cursor()
    try:
        query = "SELECT student_id, first_name, last_name, email, age, password_hash, is_active, created_at FROM students WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def update_student(
    db, student_id: int, first_name: str, last_name: str, email: str, age: int
) -> Optional[Dict[str, Any]]:
    """Update student details"""
    cursor = db.cursor()
    try:
        query = """
        UPDATE students 
        SET first_name = %s, last_name = %s, email = %s, age = %s
        WHERE student_id = %s
        RETURNING student_id, first_name, last_name, email, age, is_active, created_at
        """
        cursor.execute(query, (first_name, last_name, email, age, student_id))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_student(db, student_id: int) -> Optional[Dict[str, Any]]:
    """Delete a student"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM students WHERE student_id = %s RETURNING student_id"
        cursor.execute(query, (student_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
