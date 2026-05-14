from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status

from . import schemas, service
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: schemas.UserCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new user (requires authentication)"""
    return service.create_user(
        db, user.first_name, user.last_name, user.email, user.age
    )


@router.get("/", response_model=list[schemas.UserRead])
def list_users(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get all users (requires authentication)"""
    return service.get_users(db)


@router.get("/{user_id}", response_model=schemas.UserRead)
def get_user(
    user_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a user by ID (requires authentication)"""
    db_user = service.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.put("/{user_id}", response_model=schemas.UserRead)
def update_user(
    user_id: int,
    user: schemas.UserUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update a user (requires authentication)"""
    db_user = service.update_user(
        db, user_id, user.first_name, user.last_name, user.email, user.age
    )
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


@router.delete("/{user_id}", response_model=schemas.UserRead)
def delete_user(
    user_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a user (requires authentication)"""
    db_user = service.delete_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user


