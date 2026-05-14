from typing import List, Optional, Dict, Any
from fastapi import HTTPException, status
import logging

from app.db.query_helpers import row_to_dict, rows_to_list

logger = logging.getLogger(__name__)


def create_subject(db, subject_code: str, subject_name: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Create a new subject"""
    cursor = db.cursor()
    try:
        # Check if subject with this code already exists
        check_query = "SELECT subject_id FROM subjects WHERE subject_code = %s"
        cursor.execute(check_query, (subject_code,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Subject with this code already exists",
            )
        
        query = """
        INSERT INTO subjects (subject_code, subject_name, description)
        VALUES (%s, %s, %s)
        RETURNING subject_id, subject_code, subject_name, description, teacher_id, created_at, updated_at
        """
        cursor.execute(query, (subject_code, subject_name, description))
        result = cursor.fetchone()
        db.commit()
        logger.info(f"Subject created: {subject_name}")
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def get_subject_by_id(db, subject_id: int) -> Optional[Dict[str, Any]]:
    """Get a subject by its ID"""
    cursor = db.cursor()
    try:
        query = "SELECT subject_id, subject_code, subject_name, description, teacher_id, created_at, updated_at FROM subjects WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        result = cursor.fetchone()
        return row_to_dict(cursor.description, result)
    finally:
        cursor.close()


def get_all_subjects(db) -> List[Dict[str, Any]]:
    """Get all subjects"""
    cursor = db.cursor()
    try:
        query = "SELECT subject_id, subject_code, subject_name, description, teacher_id, created_at, updated_at FROM subjects ORDER BY subject_name"
        cursor.execute(query)
        results = cursor.fetchall()
        return rows_to_list(cursor.description, results)
    finally:
        cursor.close()


def update_subject(db, subject_id: int, subject_code: Optional[str] = None, subject_name: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """Update an existing subject"""
    cursor = db.cursor()
    try:
        subject = get_subject_by_id(db, subject_id)
        if not subject:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Subject not found",
            )
        
        # Check for duplicate subject code if updating
        if subject_code and subject_code != subject.get('subject_code'):
            check_query = "SELECT subject_id FROM subjects WHERE subject_code = %s AND subject_id != %s"
            cursor.execute(check_query, (subject_code, subject_id))
            if cursor.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Another subject with this code already exists",
                )
        
        # Build update query
        updates = []
        values = []
        if subject_code:
            updates.append("subject_code = %s")
            values.append(subject_code)
        if subject_name:
            updates.append("subject_name = %s")
            values.append(subject_name)
        if description is not None:
            updates.append("description = %s")
            values.append(description)
        
        if not updates:
            return subject
        
        values.append(subject_id)
        query = f"UPDATE subjects SET {', '.join(updates)} WHERE subject_id = %s RETURNING subject_id, subject_code, subject_name, description, teacher_id, created_at, updated_at"
        cursor.execute(query, values)
        result = cursor.fetchone()
        db.commit()
        logger.info(f"Subject updated: {result}")
        return row_to_dict(cursor.description, result)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()


def delete_subject(db, subject_id: int) -> bool:
    """Delete a subject by its ID"""
    cursor = db.cursor()
    try:
        subject = get_subject_by_id(db, subject_id)
        if not subject:
            return False
        
        query = "DELETE FROM subjects WHERE subject_id = %s"
        cursor.execute(query, (subject_id,))
        db.commit()
        logger.info(f"Subject deleted: {subject.get('subject_name')}")
        return True
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
    
    
    