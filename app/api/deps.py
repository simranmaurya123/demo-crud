import os
from typing import Generator, Dict, Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
import psycopg2

from app.db.connection import get_connection, return_connection
from app.core.config import settings
from app.core.security import verify_password
from app.api.v1.users import service as users_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_db():
    """Dependency to get database connection"""
    conn = get_connection()
    try:
        yield conn
    finally:
        return_connection(conn)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db = Depends(get_db),
) -> Dict[str, Any]:
    """Dependency to get current authenticated user"""
    secret_key = settings.JWT_SECRET_KEY
    algorithm = settings.JWT_ALGORITHM
    
    if not secret_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="JWT_SECRET_KEY is not configured",
        )

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        subject = payload.get("sub")
        if subject is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = users_service.get_user_by_email(db, subject)
    if user is None:
        raise credentials_exception
    if not user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return user
