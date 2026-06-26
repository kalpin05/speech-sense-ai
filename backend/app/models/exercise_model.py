from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from app.database import Base

class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    language = Column(String(50), nullable=False)
    content = Column(Text, nullable=False)
    difficulty = Column(String(50), default="beginner", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
