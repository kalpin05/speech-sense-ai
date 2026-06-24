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

@router.get("/therapists")
def get_all_therapists(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get all registered therapists."""
    therapists = db.query(User).filter(User.role == "therapist").all()
    return {
        "therapists": [
            {
                "id": str(t.id),
                "first_name": t.first_name,
                "last_name": t.last_name,
                "email": t.email
            }
            for t in therapists
        ]
    }

@router.get("/me/gamification")
def get_user_gamification(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get user's XP, level, progress inside level, and list of unlocked badges."""
    from app.models.badge_model import UserBadge
    badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
    badge_list = [b.badge_id for b in badges]
    return {
        "xp": current_user.xp,
        "level": current_user.level,
        "progress_pct": current_user.xp % 100,
        "badges": badge_list
    }

@router.get("/me/analytics")
def get_user_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Calculate and return session analytics and progress trends for the user."""
    sessions = db.query(TherapySession).filter(TherapySession.user_id == current_user.id).order_by(TherapySession.created_at.asc()).all()
    total_attempts = len(sessions)
    
    avg_score = 0
    best_score = 0
    if total_attempts > 0:
        avg_score = int(sum(s.accuracy_score for s in sessions) / total_attempts)
        best_score = int(max(s.accuracy_score for s in sessions))
        
    from app.services.gamification_service import calculate_streak
    streak = calculate_streak(sessions)
    
    session_data = [
        {
            "accuracy_score": s.accuracy_score,
            "created_at": s.created_at.isoformat()
        }
        for s in sessions
    ]
    
    return {
        "total_attempts": total_attempts,
        "average_score": avg_score,
        "best_score": best_score,
        "streak": streak,
        "sessions": session_data
    }


