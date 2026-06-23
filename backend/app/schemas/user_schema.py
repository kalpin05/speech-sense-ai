from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = "patient"

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: str
    therapist_id: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str | None = None


class TherapySessionResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    expected_text: str
    transcription: str
    language: str
    accuracy_score: float
    fluency_score: str
    fluency_score_val: Optional[int] = None
    speech_rate: Optional[int] = None
    pause_count: Optional[int] = None
    feedback: str
    created_at: datetime

    class Config:
        from_attributes = True
