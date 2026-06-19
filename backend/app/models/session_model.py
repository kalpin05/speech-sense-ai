from sqlalchemy import Column, String, Float, Text, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class TherapySession(Base):
    __tablename__ = "therapy_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    expected_text = Column(Text, nullable=False)
    transcription = Column(Text, nullable=False)
    language = Column(String(50), nullable=False)
    accuracy_score = Column(Float, nullable=False)
    fluency_score = Column(String(50), nullable=False)
    fluency_score_val = Column(Integer, nullable=True)
    speech_rate = Column(Integer, nullable=True)
    pause_count = Column(Integer, nullable=True)
    feedback = Column(Text, nullable=False)
    audio_file_path = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
