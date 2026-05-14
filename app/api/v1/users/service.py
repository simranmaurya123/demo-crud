from typing import Optional, Dict, Any
from app.db.query_helpers import row_to_dict, rows_to_list


def create_user(
    db,
    first_name: str,
    last_name: str,
    email: str,
    age: int,
    password_hash: Optional[str] = None,
) -> Dict[str, Any]:
    """Create a new user"""
    cursor = db.cursor()
    try:
        query = """
        INSERT INTO users (first_name, last_name, email, age, password_hash, is_active)
        VALUES (%s, %s, %s, %s, %s, TRUE)
        RETURNING user_id, first_name, last_name, email, age, password_hash, is_active, created_at
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


def get_users(db) -> list:
    """Get all users"""
    cursor = db.cursor()
    try:
        query = "SELECT user_id, first_name, last_name, email, age, is_active, created_at FROM users ORDER BY user_id"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def get_user(db, user_id: int) -> Optional[Dict[str, Any]]:
    """Get user by ID"""
    cursor = db.cursor()
    try:
        query = "SELECT user_id, first_name, last_name, email, age, is_active, created_at FROM users WHERE user_id = %s"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_user_by_email(db, email: str) -> Optional[Dict[str, Any]]:
    """Get user by email"""
    cursor = db.cursor()
    try:
        query = "SELECT user_id, first_name, last_name, email, age, password_hash, is_active, created_at FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def update_user(db, user_id: int, first_name: str, last_name: str, email: str, age: int) -> Optional[Dict[str, Any]]:
    """Update user details"""
    cursor = db.cursor()
    try:
        query = """
        UPDATE users 
        SET first_name = %s, last_name = %s, email = %s, age = %s
        WHERE user_id = %s
        RETURNING user_id, first_name, last_name, email, age, is_active, created_at
        """
        cursor.execute(query, (first_name, last_name, email, age, user_id))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_user(db, user_id: int) -> Optional[Dict[str, Any]]:
    """Delete a user"""
    cursor = db.cursor()
    try:
        query = "DELETE FROM users WHERE user_id = %s RETURNING user_id"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        db.commit()
        return row_to_dict(cursor.description, result) if result else None
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
