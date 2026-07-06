from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.session_model import TherapySession
from app.services.auth_service import get_current_user
from app.utils.exercises_db import EXERCISES_DB
import json
import logging
from uuid import UUID

log = logging.getLogger(__name__)

router = APIRouter()


@router.get("/patients")
def get_linked_patients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all patients linked to the logged-in therapist with aggregate stats."""
    if current_user.role != "therapist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Only therapists can view linked patients"
        )
        
    patients = db.query(User).filter(
        User.therapist_id == current_user.id,
        User.role == "patient"
    ).all()
    
    results = []
    for p in patients:
        # Calculate summary statistics for this patient
        sessions = db.query(TherapySession).filter(TherapySession.user_id == p.id).all()
        total_sessions = len(sessions)
        
        avg_score = 0.0
        if total_sessions > 0:
            avg_score = sum(s.accuracy_score for s in sessions) / total_sessions
            
        last_practice = None
        if total_sessions > 0:
            # Sort sessions by created_at to find the most recent
            sorted_sessions = sorted(sessions, key=lambda s: s.created_at, reverse=True)
            last_practice = sorted_sessions[0].created_at
            
        results.append({
            "id": str(p.id),
            "email": p.email,
            "first_name": p.first_name,
            "last_name": p.last_name,
            "total_sessions": total_sessions,
            "average_score": round(avg_score, 2),
            "last_practice": last_practice,
            "created_at": p.created_at
        })
        
    return {"patients": results}


@router.get("/patients/{patient_id}/sessions")
def get_patient_sessions(
    patient_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all therapy sessions of a specific linked patient."""
    if current_user.role != "therapist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Only therapists can view patient sessions"
        )
        
    # Verify patient is linked to this therapist
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        
    if patient.therapist_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Patient is not linked to you"
        )
        
    sessions = db.query(TherapySession).filter(
        TherapySession.user_id == patient_id
    ).order_by(TherapySession.created_at.desc()).all()
    
    results = []
    for s in sessions:
        results.append({
            "id": str(s.id),
            "expected_text": s.expected_text,
            "transcription": s.transcription,
            "language": s.language,
            "accuracy_score": s.accuracy_score,
            "fluency_score": s.fluency_score,
            "fluency_score_val": s.fluency_score_val,
            "speech_rate": s.speech_rate,
            "pause_count": s.pause_count,
            "feedback": s.feedback,
            "confidence_score": s.confidence_score,
            "nervousness_score": s.nervousness_score,
            "hesitation_score": s.hesitation_score,
            "emotion": s.emotion,
            "created_at": s.created_at
        })
        
    return {"sessions": results}


@router.get("/patients/{patient_id}/adaptive")
def get_patient_adaptive(
    patient_id: UUID,
    language: str = "english",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the adaptive analysis (weak words, sounds, recommended exercises) for a linked patient."""
    if current_user.role != "therapist":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Only therapists can view patient recommendations"
        )
        
    # Verify patient is linked to this therapist
    patient = db.query(User).filter(User.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")
        
    if patient.therapist_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Patient is not linked to you"
        )
        
    # Aggregate logic similar to get_adaptive_exercises
    sessions = db.query(TherapySession).filter(
        TherapySession.user_id == patient_id,
        TherapySession.language.ilike(language)
    ).order_by(TherapySession.created_at.desc()).limit(10).all()
    
    word_counts = {}
    for s in sessions:
        try:
            fb_data = json.loads(s.feedback)
            inc_words = fb_data.get("incorrect_words", [])
            for w in inc_words:
                w_clean = w.lower().strip()
                if w_clean:
                    word_counts[w_clean] = word_counts.get(w_clean, 0) + 1
        except Exception:
            continue
            
    sorted_weak_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    weak_words = [w for w, count in sorted_weak_words]
    
    sound_patterns = ["th", "sh", "ch", "wh", "ph", "tr", "pl", "gr", "st", "sp", "h", "s", "f", "r", "l", "w", "v"]
    sound_counts = {}
    for w in weak_words:
        for pattern in sound_patterns:
            if w.startswith(pattern):
                sound_counts[pattern] = sound_counts.get(pattern, 0) + 1
                break
                
    sorted_weak_sounds = sorted(sound_counts.items(), key=lambda x: x[1], reverse=True)
    weak_sounds = [sound for sound, count in sorted_weak_sounds if count >= 1]
    
    top_weak_words = weak_words[:5]
    top_weak_sounds = weak_sounds[:3]
    
    recommended_exercises = []
    exercises_list = []
    lang_key = language.lower()
    if lang_key not in EXERCISES_DB:
        lang_key = "english"
        
    for diff, items in EXERCISES_DB[lang_key].items():
        exercises_list.extend(items)
        
    for ex in exercises_list:
        ex_lower = ex.lower()
        has_weak_word = any(w in ex_lower for w in top_weak_words)
        if has_weak_word:
            recommended_exercises.append(ex)
            
    recommended_exercises = list(set(recommended_exercises))[:3]
    
    return {
        "weak_words": top_weak_words,
        "weak_sounds": top_weak_sounds,
        "recommended_exercises": recommended_exercises
    }
