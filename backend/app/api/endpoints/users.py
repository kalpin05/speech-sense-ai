from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from app.database import get_db
from app.models.user import User
from app.models.settings_model import UserSettings
from app.models.session_model import TherapySession
from app.schemas.settings_schema import UserSettingsResponse, UserSettingsUpdate, ProfileUpdate
from app.services.auth_service import get_current_user
import logging

log = logging.getLogger(__name__)

router = APIRouter()

@router.get("/me/settings", response_model=UserSettingsResponse)
def get_user_settings(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Fetch user settings. Create default if missing."""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
        db.commit()
        db.refresh(settings)
    return settings

@router.put("/me/settings", response_model=UserSettingsResponse)
def update_user_settings(payload: UserSettingsUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update user settings."""
    settings = db.query(UserSettings).filter(UserSettings.user_id == current_user.id).first()
    if not settings:
        settings = UserSettings(user_id=current_user.id)
        db.add(settings)
    
    for key, value in payload.model_dump().items():
        setattr(settings, key, value)
    
    db.commit()
    db.refresh(settings)
    return settings

@router.put("/me/profile")
def update_profile(payload: ProfileUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Update the user's first name."""
    current_user.first_name = payload.first_name
    db.commit()
    db.refresh(current_user)
    return {"status": "success", "first_name": current_user.first_name}

class LinkTherapistRequest(BaseModel):
    therapist_email: EmailStr

@router.delete("/me/data")
def delete_user_data(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Reset App: Delete all past therapy sessions for this user."""
    deleted_count = db.query(TherapySession).filter(TherapySession.user_id == current_user.id).delete()
    db.commit()
    return {"status": "success", "deleted_sessions": deleted_count}

@router.put("/me/link-therapist")
def link_therapist(payload: LinkTherapistRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Link current patient to a therapist by email."""
    if current_user.role != "patient":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only patients can link to a therapist")
        
    therapist = db.query(User).filter(User.email == payload.therapist_email).first()
    if not therapist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Therapist not found")
        
    if therapist.role != "therapist":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Target user is not registered as a therapist")
        
    current_user.therapist_id = therapist.id
    db.commit()
    db.refresh(current_user)
    return {
        "status": "success",
        "therapist": {
            "first_name": therapist.first_name,
            "last_name": therapist.last_name,
            "email": therapist.email
        }
    }

@router.delete("/me/link-therapist")
def unlink_therapist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Unlink current patient from their therapist."""
    if current_user.role != "patient":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only patients can unlink a therapist")
        
    current_user.therapist_id = None
    db.commit()
    db.refresh(current_user)
    return {"status": "success", "message": "Therapist unlinked"}

@router.get("/me/therapist")
def get_linked_therapist(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the details of the linked therapist."""
    if current_user.therapist_id is None:
        return {"therapist": None}
        
    therapist = db.query(User).filter(User.id == current_user.therapist_id).first()
    if not therapist:
        return {"therapist": None}
        
    return {
        "therapist": {
            "first_name": therapist.first_name,
            "last_name": therapist.last_name,
            "email": therapist.email
        }
    }
