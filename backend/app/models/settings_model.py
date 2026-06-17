from sqlalchemy import Column, Boolean, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import Base
import uuid

class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    daily_goal = Column(Integer, default=5)
    reminders = Column(Boolean, default=False)
    sound = Column(Boolean, default=True)
    mic_sensitivity = Column(Integer, default=5)
    xp_boost = Column(Boolean, default=False)
    streak_freeze = Column(Boolean, default=False)
    light_mode = Column(Boolean, default=False)
    save_data = Column(Boolean, default=True)
