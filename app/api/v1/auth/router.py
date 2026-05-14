import logging
from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, status, Form

from . import schemas, service
from app.api.deps import get_db, get_current_user
from app.core.security import hash_password, verify_password, create_access_token
from app.api.v1.users import service as users_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=schemas.Token, status_code=status.HTTP_201_CREATED)
def register(user: schemas.UserRegister, db: Any = Depends(get_db)):
    """Register a new user"""
    existing_user = users_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    password_hash = hash_password(user.password)
    new_user = service.register_user(
        db,
        user.first_name,
        user.last_name,
        user.email,
        user.age,
        password_hash,
    )
    
    access_token = create_access_token(subject=new_user["email"])
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post(
    "/login",
    response_model=schemas.Token,
    summary="User Login",
    description="Authenticate user with email and password to get access token"
)
def login(username: str = Form(...), password: str = Form(...), db: Any = Depends(get_db)):
    """User login endpoint"""
    logger.info(f"Login attempt for user: {username}")
    
    db_user = users_service.get_user_by_email(db, username)
    if not db_user or not db_user.get("password_hash"):
        logger.warning(
            f"Login failed: User not found or no password hash for {username}"
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(password, db_user["password_hash"]):
        logger.warning(f"Login failed: Invalid password for {username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(subject=db_user["email"])
    logger.info(f"Login successful for user: {username}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.get("/me", response_model=schemas.TokenData)
def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current authenticated user info"""
    return {"subject": current_user["email"]}


