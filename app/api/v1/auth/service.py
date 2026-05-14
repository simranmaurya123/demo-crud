from typing import Optional, Dict, Any
from app.api.v1.users import service as users_service


def register_user(
    db,
    first_name: str,
    last_name: str,
    email: str,
    age: int,
    password_hash: str,
) -> Dict[str, Any]:
    """Register a new user with password"""
    return users_service.create_user(
        db, first_name, last_name, email, age, password_hash=password_hash
    )


def authenticate_user(db, email: str) -> Optional[Dict[str, Any]]:
    """Get user by email for authentication"""
    return users_service.get_user_by_email(db, email)
