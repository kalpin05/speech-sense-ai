from sqlalchemy import Column, String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
from app.database import Base
from app.models.language_progress import UserLanguageProgress

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(50), default="patient", server_default="patient", nullable=False)
    therapist_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    xp = Column(Integer, default=0, server_default="0", nullable=False)
    level = Column(Integer, default=1, server_default="1", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    language_progress = relationship("UserLanguageProgress", back_populates="user", cascade="all, delete-orphan")


