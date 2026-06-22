from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.concurrency import run_in_threadpool
import asyncio
from starlette.staticfiles import StaticFiles
import os
import shutil
import uuid
import logging

from app.services.whisper_service import transcribe_audio, transcribe_audio_detailed
from app.services.analysis_service import (
    calculate_accuracy,
    calculate_fluency,
    calculate_real_fluency,
    generate_feedback
)
from app.utils.language_map import LANGUAGE_MAP
from app.database import engine, Base, get_db
from sqlalchemy.orm import Session
from app.api.endpoints import auth, users
from app.models import user, session_model
from app.models.session_model import TherapySession
from app.schemas.user_schema import UserResponse, TherapySessionResponse
from app.utils.file_handler import is_valid_audio, sanitize_extension
from app.services.auth_service import get_current_user
from app.config import ALLOW_CREATE_ALL

# Limit to 1 concurrent Whisper transcription to prevent Out-Of-Memory crashes
whisper_semaphore = asyncio.Semaphore(1)

# Only initialize DB schema when explicitly allowed (safer for production)
if ALLOW_CREATE_ALL:
    Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure CORS from environment
_allow_all = os.getenv("ALLOW_ALL_ORIGINS", "false").lower() in ("1", "true", "yes")
if _allow_all:
    cors_origins = ["*"]
    allow_credentials = False
else:
    raw = os.getenv("ALLOWED_ORIGINS", "")
    if not raw:
        raw = "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000,http://127.0.0.1:3000"
    cors_origins = [o.strip() for o in raw.split(",") if o.strip()]
    
    # Always ensure default local development origins are allowed
    default_dev_origins = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    for o in default_dev_origins:
        if o not in cors_origins:
            cors_origins.append(o)
            
    allow_credentials = os.getenv("ALLOW_CREDENTIALS", "false").lower() in ("1", "true", "yes")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])

# Upload folder (kept inside backend/uploads)
UPLOAD_FOLDER = Path(__file__).resolve().parents[1] / "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"

log = logging.getLogger("uvicorn.error")
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))


@app.get("/health")
def health():
    return {"message": "Speech Therapy API Running"}


@app.post("/analyze")
async def analyze_audio(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    expected_text: str = Form(...),
    language: str = Form(...),
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)
):
    # Limits and checks
    MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE", 10 * 1024 * 1024))  # 10MB default

    if language.lower() not in LANGUAGE_MAP:
        raise HTTPException(status_code=400, detail="Unsupported language")

    language_code = LANGUAGE_MAP[language.lower()]

    ext = sanitize_extension(file.filename)
    if not ext:
        raise HTTPException(status_code=400, detail="Invalid or unsupported file format")

    # Build a safe unique filename
    safe_name = f"{uuid.uuid4().hex}{ext}"
    file_path = str(UPLOAD_FOLDER / safe_name)

    # Stream upload with size check
    try:
        total = 0
        with open(file_path, "wb") as buffer:
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                total += len(chunk)
                if total > MAX_UPLOAD_SIZE:
                    buffer.close()
                    try:
                        os.remove(file_path)
                    except Exception:
                        pass
                    raise HTTPException(status_code=413, detail="Uploaded file is too large")
                buffer.write(chunk)

        # Register background cleanup task so the disk doesn't fill up
        def cleanup_file(path: str):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                log.error(f"Failed to cleanup file {path}: {e}")
                
        background_tasks.add_task(cleanup_file, file_path)

        # Controlled transcription using threadpool to prevent freezing the event loop
        # and using Semaphore to prevent Out-Of-Memory crashes
        try:
            async with whisper_semaphore:
                whisper_result = await run_in_threadpool(transcribe_audio_detailed, file_path, language_code)
                transcription = whisper_result.get("text", "").strip()
        except Exception as e:
            log.exception("Transcription failed")
            raise HTTPException(status_code=500, detail="Transcription service failed")

        # Analysis
        accuracy = calculate_accuracy(expected_text, transcription)
        
        # Real fluency metrics (speech rate, pause duration/count)
        fluency_data = calculate_real_fluency(file_path, transcription, language_code)
        fluency = fluency_data["category"]
        fluency_score_val = fluency_data["fluency_score"]
        speech_rate = fluency_data["speech_rate"]
        pause_count = fluency_data["pause_count"]

        feedback = generate_feedback(expected_text, transcription, accuracy, language_code, whisper_result=whisper_result)

        # Save to database
        db_session = TherapySession(
            user_id=current_user.id,
            expected_text=expected_text,
            transcription=transcription,
            language=language,
            accuracy_score=accuracy,
            fluency_score=fluency,
            fluency_score_val=fluency_score_val,
            speech_rate=speech_rate,
            pause_count=pause_count,
            feedback=feedback,
            audio_file_path=file_path
        )
        try:
            db.add(db_session)
            db.commit()
        except Exception:
            db.rollback()
            log.exception("Database commit failed for new therapy session")
            raise HTTPException(status_code=500, detail="Failed to save session")

        return {
            "status": "success",
            "language": language,
            "transcription": transcription,
            "accuracy": accuracy,
            "fluency": fluency,
            "fluency_score": fluency_score_val,
            "speech_rate": speech_rate,
            "pause_count": pause_count,
            "feedback": feedback
        }

    except HTTPException:
        raise
    except Exception:
        log.exception("Unexpected error in /analyze")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/users")
def get_all_users(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    users = db.query(user.User).offset(skip).limit(limit).all()
    safe = []
    for u in users:
        safe.append({
            "id": str(u.id),
            "email": u.email,
            "first_name": u.first_name,
            "last_name": u.last_name,
            "created_at": u.created_at,
        })
    return {"users_in_database": safe}

@app.get("/sessions")
def get_all_sessions(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    sessions = db.query(session_model.TherapySession).offset(skip).limit(limit).all()
    safe = []
    for s in sessions:
        safe.append({
            "id": str(s.id),
            "user_id": str(s.user_id) if s.user_id else None,
            "expected_text": s.expected_text,
            "transcription": s.transcription,
            "language": s.language,
            "accuracy_score": s.accuracy_score,
            "fluency_score": s.fluency_score,
            "fluency_score_val": s.fluency_score_val,
            "speech_rate": s.speech_rate,
            "pause_count": s.pause_count,
            "feedback": s.feedback,
            "created_at": s.created_at,
        })
    return {"sessions_in_database": safe}


@app.get("/users/me/sessions")
def get_my_sessions(db: Session = Depends(get_db), current_user: user.User = Depends(get_current_user)):
    """Fetch the past therapy sessions for the logged in user."""
    sessions = db.query(session_model.TherapySession).filter(session_model.TherapySession.user_id == current_user.id).order_by(session_model.TherapySession.created_at.desc()).all()
    safe = []
    for s in sessions:
        safe.append({
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
            "created_at": s.created_at,
        })
    return {"my_sessions": safe}


EXERCISES_DB = {
    "english": {
        "beginner": [
            "The quick brown fox jumps over the lazy dog.",
            "Hello, how are you today?",
            "She sells sea shells by the sea shore."
        ],
        "intermediate": [
            "I would like to order a cup of coffee and a croissant.",
            "Reading books is a great way to expand your vocabulary.",
            "Practice makes perfect when learning a new language."
        ],
        "advanced": [
            "Technology is evolving at an unprecedented pace.",
            "Continuous learning is essential for personal growth.",
            "Pneumonoultramicroscopicslicovolcanoconiosis is a long word."
        ]
    },
    "hindi": {
        "beginner": [
            "मेरा नाम राहुल है और मैं दिल्ली में रहता हूँ।",
            "नमस्ते, आप कैसे हैं?"
        ],
        "intermediate": [
            "मुझे भारतीय भोजन बहुत पसंद है।",
            "ज्ञान सबसे बड़ा धन है।"
        ],
        "advanced": [
            "कल बारिश होने की संभावना है।",
            "वैज्ञानिक अनुसंधान निरंतर प्रगति कर रहा है।"
        ]
    },
    "spanish": {
        "beginner": [
            "Hola, ¿cómo estás hoy?",
            "Buenos días a todos."
        ],
        "intermediate": [
            "Me gustaría una cerveza, por favor.",
            "El aprendizaje de idiomas abre muchas puertas."
        ],
        "advanced": [
            "El clima es muy agradable en verano.",
            "La tecnología avanza a un ritmo sin precedentes."
        ]
    }
}


@app.get("/exercises")
def get_exercises(language: str = "english", difficulty: str = None):
    """Return some predefined exercises for the user to read based on language and difficulty."""
    lang = language.lower()
    if lang not in EXERCISES_DB:
        lang = "english"
        
    db_by_lang = EXERCISES_DB[lang]
    
    if difficulty:
        diff = difficulty.lower()
        if diff in db_by_lang:
            return {"exercises": db_by_lang[diff]}
        # If invalid difficulty, fall back to empty list
        return {"exercises": []}
        
    # If no difficulty specified, return all flattened exercises for backward compatibility
    all_ex = []
    for diff, items in db_by_lang.items():
        all_ex.extend(items)
    return {"exercises": all_ex}


@app.get("/exercises/adaptive")
def get_adaptive_exercises(
    language: str = "english",
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)
):
    """Analyze recent user sessions to extract weak words, sounds and generate adaptive exercises."""
    import json
    
    # 1. Fetch user's last 10 therapy sessions for this language
    sessions = db.query(TherapySession).filter(
        TherapySession.user_id == current_user.id,
        TherapySession.language.ilike(language)
    ).order_by(TherapySession.created_at.desc()).limit(10).all()
    
    # 2. Extract incorrect words from session feedback
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
            
    # Sort weak words by frequency of error
    sorted_weak_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    weak_words = [w for w, count in sorted_weak_words]
    
    # 3. Identify weak sounds (prefixes or common consonant combinations)
    sound_patterns = ["th", "sh", "ch", "wh", "ph", "tr", "pl", "gr", "st", "sp", "h", "s", "f", "r", "l", "w", "v"]
    sound_counts = {}
    
    for w in weak_words:
        for pattern in sound_patterns:
            if w.startswith(pattern):
                sound_counts[pattern] = sound_counts.get(pattern, 0) + 1
                break
                
    # Sort weak sounds by frequency
    sorted_weak_sounds = sorted(sound_counts.items(), key=lambda x: x[1], reverse=True)
    weak_sounds = [sound for sound, count in sorted_weak_sounds if count >= 1]
    
    # Limit to top 5 weak words and top 3 weak sounds to avoid UI clutter
    top_weak_words = weak_words[:5]
    top_weak_sounds = weak_sounds[:3]
    
    # 4. Generate custom practice drill
    if top_weak_words:
        words_str = ", ".join(top_weak_words)
        custom_drill = f"Practice saying these words: {words_str}"
    else:
        custom_drill = "Excellent job! No weak words detected yet."
        
    # 5. Retrieve recommended predefined exercises containing any of their weak words
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
        "custom_drill": custom_drill,
        "recommended_exercises": recommended_exercises
    }

# Mount frontend static files LAST so it doesn't intercept API routes
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")