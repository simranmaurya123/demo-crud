from typing import Optional, Dict, Any, List
from app.db.query_helpers import row_to_dict, rows_to_list


def create_teacher(
    db,
    first_name: str,
    last_name: str,
    email: str,
    age: int,
    password_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new teacher"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO teachers (first_name, last_name, email, age, password_hash, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        RETURNING teacher_id, first_name, last_name, email, age, password_hash, is_active, created_at
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


def get_teachers(db) -> List[Dict[str, Any]]:
    """Get all teachers"""
    cursor = db.cursor()
    try:
        query = "SELECT teacher_id, first_name, last_name, email, age, is_active, created_at FROM teachers ORDER BY teacher_id"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_teacher(db, teacher_id: int) -> Optional[Dict[str, Any]]:
    """Get teacher by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT teacher_id, first_name, last_name, email, age, is_active, created_at FROM teachers WHERE teacher_id = %s"
        cursor.execute(query, (teacher_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_teacher_by_email(db, email: str) -> Optional[Dict[str, Any]]:
    """Get teacher by email"""
    cursor = db.cursor()
    try:
        query = "SELECT teacher_id, first_name, last_name, email, age, password_hash, is_active, created_at FROM teachers WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def update_teacher(
    db, teacher_id: int, first_name: str, last_name: str, email: str, age: int
) -> Optional[Dict[str, Any]]:
    """Update teacher details"""
    cursor = db.cursor()
    try:
        query = """
        UPDATE teachers 
        SET first_name = %s, last_name = %s, email = %s, age = %s
        WHERE teacher_id = %s
        RETURNING teacher_id, first_name, last_name, email, age, is_active, created_at
        """
        cursor.execute(query, (first_name, last_name, email, age, teacher_id))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_teacher(db, teacher_id: int) -> Optional[Dict[str, Any]]:
    """Delete a teacher"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM teachers WHERE teacher_id = %s RETURNING teacher_id"
        cursor.execute(query, (teacher_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
