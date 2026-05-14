import logging
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from app.api.deps import get_db, get_current_user
from . import schemas, service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subjects", tags=["Subjects"])

@router.post(
    "/",
    response_model=schemas.SubjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create Subject",
    description="Create a new subject with a unique name"
)
def create_subject(
    subject: schemas.SubjectCreate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Create a new subject"""
    db_subject = service.create_subject(db, subject.subject_code, subject.subject_name, subject.description)
    logger.info(f"Subject created: {subject.subject_name}")
    return db_subject

@router.get(
    "/",    
    response_model=list[schemas.SubjectResponse],
    summary="List Subjects",        
    description="Get a list of all subjects"
)
def list_subjects(
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a list of all subjects"""
    db_subjects = service.get_all_subjects(db)
    logger.info(f"{len(db_subjects)} subjects retrieved")
    return db_subjects

@router.get(
    "/{subject_id}",
    response_model=schemas.SubjectResponse,
    summary="Get Subject",
    description="Get a specific subject by ID"
)
def get_subject(
    subject_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Get a specific subject"""
    db_subject = service.get_subject_by_id(db, subject_id)
    if not db_subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    logger.info(f"Subject retrieved: {db_subject.subject_name}")
    return db_subject

@router.put(
    "/{subject_id}",  
    response_model=schemas.SubjectResponse,
    summary="Update Subject",
    description="Update an existing subject's name and/or description"
)
def update_subject(
    subject_id: int,
    subject_update: schemas.SubjectUpdate,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Update an existing subject"""
    db_subject = service.update_subject(db, subject_id, subject_update.subject_code, subject_update.subject_name, subject_update.description)
    logger.info(f"Subject updated: {db_subject.subject_name}")
    return db_subject

@router.delete(
    "/{subject_id}",
    response_model=schemas.SubjectDeleteResponse,
    summary="Delete Subject",
    description="Delete a subject by its ID"
)
def delete_subject(
    subject_id: int,
    db: Any = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """Delete a subject by its ID"""
    success = service.delete_subject(db, subject_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    logger.info(f"Subject deleted: {subject_id}")
    return {"message": "Subject deleted successfully"}



