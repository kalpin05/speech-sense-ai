from pydantic import BaseModel
from uuid import UUID

class UserSettingsBase(BaseModel):
    daily_goal: int
    reminders: bool
    sound: bool
    mic_sensitivity: int
    xp_boost: bool
    streak_freeze: bool
    light_mode: bool
    save_data: bool

class UserSettingsUpdate(UserSettingsBase):
    pass

class UserSettingsResponse(UserSettingsBase):
    id: UUID
    user_id: UUID

    class Config:
        from_attributes = True

class ProfileUpdate(BaseModel):
    first_name: str
