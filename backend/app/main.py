from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
import os
import shutil

from app.services.whisper_service import transcribe_audio
from app.services.analysis_service import (
    calculate_accuracy,
    calculate_fluency,
    generate_feedback
)
from app.utils.language_map import LANGUAGE_MAP
from app.database import engine, Base, get_db
from sqlalchemy.orm import Session
from fastapi import Depends
from app.api.endpoints import auth
from app.models import user, session_model
from app.models.session_model import TherapySession

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

frontend_dir = Path(__file__).resolve().parents[2] / "frontend"
app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")


@app.get("/health")
def health():
    return {"message": "Speech Therapy API Running"}


@app.post("/analyze")
async def analyze_audio(
    file: UploadFile = File(...),
    expected_text: str = Form(...),
    language: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if not file.filename.endswith((".wav", ".mp3", ".m4a", ".mp4")):
            return {"status": "error", "message": "Invalid file format"}

        if language.lower() not in LANGUAGE_MAP:
            return {"status": "error", "message": "Unsupported language"}

        language_code = LANGUAGE_MAP[language.lower()]

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 🔥 Controlled transcription
        transcription = transcribe_audio(file_path, language_code)

        # Analysis
        accuracy = calculate_accuracy(expected_text, transcription)
        fluency = calculate_fluency(transcription, language_code)
        feedback = generate_feedback(expected_text, transcription, accuracy, language_code)

        # Save to database
        db_session = TherapySession(
            expected_text=expected_text,
            transcription=transcription,
            language=language,
            accuracy_score=accuracy,
            fluency_score=fluency,
            feedback=feedback,
            audio_file_path=file_path
        )
        db.add(db_session)
        db.commit()

        return {
            "status": "success",
            "language": language,
            "transcription": transcription,
            "accuracy": accuracy,
            "fluency": fluency,
            "feedback": feedback
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(user.User).all()
    return {"users_in_database": users}

@app.get("/sessions")
def get_all_sessions(db: Session = Depends(get_db)):
    sessions = db.query(session_model.TherapySession).all()
    return {"sessions_in_database": sessions}