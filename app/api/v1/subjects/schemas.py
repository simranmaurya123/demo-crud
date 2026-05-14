from typing import Optional
from pydantic import BaseModel
from datetime import date, datetime

class SubjectBase(BaseModel):
    subject_code: str
    subject_name: str
    description: Optional[str] = None

class SubjectCreate(SubjectBase):
    pass

class SubjectUpdate(BaseModel):
    subject_code: Optional[str] = None
    subject_name: Optional[str] = None
    description: Optional[str] = None

class SubjectResponse(SubjectBase):
    subject_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class SubjectDeleteResponse(BaseModel):
    message: str