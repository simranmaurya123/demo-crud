"""
Helper utilities for database operations with raw SQL
"""


def row_to_dict(cursor_description, row):
    """
    Convert a database row tuple to a dictionary
    
    Args:
        cursor_description: cursor.description from psycopg2
        row: A single row tuple from database query
    
    Returns:
        Dictionary with column names as keys
    """
    if row is None:
        return None
    
    column_names = [desc[0] for desc in cursor_description]
    return dict(zip(column_names, row))


def rows_to_list(cursor_description, rows):
    """
    Convert multiple database rows to list of dictionaries
    
    Args:
        cursor_description: cursor.description from psycopg2
        rows: Multiple row tuples from database query
    
    Returns:
        List of dictionaries
    """
    if not rows:
        return []
    
    column_names = [desc[0] for desc in cursor_description]
    return [dict(zip(column_names, row)) for row in rows]
