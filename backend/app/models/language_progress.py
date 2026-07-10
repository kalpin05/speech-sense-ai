import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Date, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base

class UserLanguageProgress(Base):
    __tablename__ = "user_language_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language = Column(String, nullable=False)  # e.g., 'english', 'spanish', 'hindi'
    xp = Column(Integer, default=0, nullable=False)
    level = Column(Integer, default=1, nullable=False)
    streak = Column(Integer, default=0, nullable=False)
    last_attempt_date = Column(Date, nullable=True)

    # Relationships
    user = relationship("User", back_populates="language_progress")

    # Add Unique constraint on (user_id, language)
    __table_args__ = (
        UniqueConstraint("user_id", "language", name="uq_user_language"),
    )
