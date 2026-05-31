from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
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
    feedback: str
    created_at: datetime

    class Config:
        from_attributes = True
