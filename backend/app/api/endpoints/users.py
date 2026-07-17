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
def get_user_gamification(
    language: str = "english",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user's XP, level, progress inside level, and list of unlocked badges for a specific language."""
    from app.models.badge_model import UserBadge
    from app.models.language_progress import UserLanguageProgress

    lang_clean = language.lower().strip()
    
    # Fetch or create language-specific progress record
    prog = db.query(UserLanguageProgress).filter(
        UserLanguageProgress.user_id == current_user.id,
        UserLanguageProgress.language == lang_clean
    ).first()
    
    if not prog:
        prog = UserLanguageProgress(
            user_id=current_user.id,
            language=lang_clean,
            xp=0,
            level=1,
            streak=0
        )
        db.add(prog)
        db.commit()
        db.refresh(prog)
        
    badges = db.query(UserBadge).filter(UserBadge.user_id == current_user.id).all()
    badge_list = [b.badge_id for b in badges]
    
    return {
        "xp": prog.xp,
        "level": prog.level,
        "progress_pct": prog.xp % 100,
        "badges": badge_list,
        "global_xp": current_user.xp,
        "global_level": current_user.level
    }

@router.get("/me/analytics")
def get_user_analytics(
    language: str = "english",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Calculate and return session analytics and progress trends for the user, filtered by language."""
    lang_clean = language.lower().strip()
    
    sessions = db.query(TherapySession).filter(
        TherapySession.user_id == current_user.id,
        TherapySession.language.ilike(lang_clean)
    ).order_by(TherapySession.created_at.asc()).all()
    
    total_attempts = len(sessions)
    
    avg_score = 0
    best_score = 0
    avg_confidence = 0
    avg_nervousness = 0
    avg_hesitation = 0
    emotion_breakdown = {}
    
    if total_attempts > 0:
        avg_score = int(sum(s.accuracy_score for s in sessions) / total_attempts)
        best_score = int(max(s.accuracy_score for s in sessions))
        
        conf_vals = [s.confidence_score for s in sessions if s.confidence_score is not None]
        nerv_vals = [s.nervousness_score for s in sessions if s.nervousness_score is not None]
        hes_vals = [s.hesitation_score for s in sessions if s.hesitation_score is not None]
        
        avg_confidence = int(sum(conf_vals) / len(conf_vals)) if conf_vals else 0
        avg_nervousness = int(sum(nerv_vals) / len(nerv_vals)) if nerv_vals else 0
        avg_hesitation = int(sum(hes_vals) / len(hes_vals)) if hes_vals else 0
        
        for s in sessions:
            if s.emotion:
                emotion_clean = s.emotion.lower()
                emotion_breakdown[emotion_clean] = emotion_breakdown.get(emotion_clean, 0) + 1
        
    from app.services.gamification_service import calculate_streak
    streak = calculate_streak(sessions)
    
    session_data = [
        {
            "accuracy_score": s.accuracy_score,
            "fluency_score_val": s.fluency_score_val,
            "confidence_score": s.confidence_score,
            "nervousness_score": s.nervousness_score,
            "hesitation_score": s.hesitation_score,
            "emotion": s.emotion,
            "created_at": s.created_at.isoformat()
        }
        for s in sessions
    ]
    
    return {
        "total_attempts": total_attempts,
        "average_score": avg_score,
        "best_score": best_score,
        "streak": streak,
        "average_confidence": avg_confidence,
        "average_nervousness": avg_nervousness,
        "average_hesitation": avg_hesitation,
        "emotion_breakdown": emotion_breakdown,
        "sessions": session_data
    }


@router.get("/me/practice-heatmap")
def get_user_practice_heatmap(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve daily practice session counts for the last 180 days to populate the consistency heatmap."""
    from datetime import datetime, timedelta
    from sqlalchemy import func
    
    # Start date is 180 days ago
    start_date = datetime.utcnow() - timedelta(days=180)
    
    # Query sessions grouped by date
    results = db.query(
        func.date(TherapySession.created_at).label("date"),
        func.count(TherapySession.id).label("count")
    ).filter(
        TherapySession.user_id == current_user.id,
        TherapySession.created_at >= start_date
    ).group_by(
        func.date(TherapySession.created_at)
    ).all()
    
    # Format as dictionary mapping YYYY-MM-DD -> count
    heatmap_data = {str(r.date): r.count for r in results}
    
    return {"heatmap": heatmap_data}


class GameScoreRequest(BaseModel):
    score: int
    language: str = "english"


@router.post("/me/game-score")
def record_game_score(
    payload: GameScoreRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Log a voice game session, credit XP to the user globally and for the target language, and update level."""
    from app.models.language_progress import UserLanguageProgress
    
    # Calculate XP reward based on game score
    # 1 XP per point scored, max 20 XP per session to avoid exploits
    xp_gained = min(20, max(5, payload.score // 5))
    
    # Credit global XP
    current_user.xp += xp_gained
    current_user.level = (current_user.xp // 100) + 1
    
    # Credit language-specific XP
    lang_clean = payload.language.lower().strip()
    prog = db.query(UserLanguageProgress).filter(
        UserLanguageProgress.user_id == current_user.id,
        UserLanguageProgress.language == lang_clean
    ).first()
    
    if not prog:
        prog = UserLanguageProgress(
            user_id=current_user.id,
            language=lang_clean,
            xp=0,
            level=1,
            streak=0
        )
        db.add(prog)
        
    prog.xp += xp_gained
    prog.level = (prog.xp // 100) + 1
    
    db.commit()
    
    return {
        "status": "success",
        "xp_gained": xp_gained,
        "global_xp": current_user.xp,
        "global_level": current_user.level,
        "lang_xp": prog.xp,
        "lang_level": prog.level
    }


