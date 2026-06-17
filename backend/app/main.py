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

from app.services.whisper_service import transcribe_audio
from app.services.analysis_service import (
    calculate_accuracy,
    calculate_fluency,
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
    raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8000")
    cors_origins = [o.strip() for o in raw.split(",") if o.strip()]
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
                transcription = await run_in_threadpool(transcribe_audio, file_path, language_code)
        except Exception as e:
            log.exception("Transcription failed")
            raise HTTPException(status_code=500, detail="Transcription service failed")

        # Analysis
        accuracy = calculate_accuracy(expected_text, transcription)
        fluency = calculate_fluency(transcription, language_code)
        feedback = generate_feedback(expected_text, transcription, accuracy, language_code)

        # Save to database
        db_session = TherapySession(
            user_id=current_user.id,
            expected_text=expected_text,
            transcription=transcription,
            language=language,
            accuracy_score=accuracy,
            fluency_score=fluency,
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
            "feedback": s.feedback,
            "created_at": s.created_at,
        })
    return {"my_sessions": safe}


@app.get("/exercises")
def get_exercises(language: str = "english"):
    """Return some predefined exercises for the user to read based on language."""
    # Hardcoded exercises for MVP. In production, move these to a Database table.
    exercises_db = {
        "english": [
            "The quick brown fox jumps over the lazy dog.",
            "I would like to order a cup of coffee and a croissant.",
            "Technology is evolving at an unprecedented pace."
        ],
        "hindi": [
            "मेरा नाम राहुल है और मैं दिल्ली में रहता हूँ।",
            "मुझे भारतीय भोजन बहुत पसंद है।",
            "कल बारिश होने की संभावना है।"
        ],
        "spanish": [
            "Hola, ¿cómo estás hoy?",
            "Me gustaría una cerveza, por favor.",
            "El clima es muy agradable en verano."
        ]
    }
    lang = language.lower()
    return {"exercises": exercises_db.get(lang, exercises_db["english"])}

# Mount frontend static files LAST so it doesn't intercept API routes
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")