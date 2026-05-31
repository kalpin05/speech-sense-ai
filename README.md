# Speech Therapy API

This repository contains a FastAPI backend and a simple frontend for a speech therapy transcription and analysis service.

## Overview
- Backend: FastAPI application in `backend/app`
- Frontend: static files in `frontend`
- Transcription: uses Whisper (lazy-loaded) to transcribe uploaded audio
- Analysis: accuracy and fluency heuristics

## Setup
1. Create a Python environment (recommended: Python 3.10+)

```bash
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. Set required environment variables (example .env)

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/speech-ai
SECRET_KEY=change-me-to-a-secret-value
ALLOWED_ORIGINS=http://localhost:3000
ALLOW_CREDENTIALS=true
MAX_UPLOAD_SIZE=10485760
```

3. (Optional) To allow the app to run `Base.metadata.create_all()` on startup for local testing, set:

```
ALLOW_CREATE_ALL=true
```

Note: For production use, set up Alembic migrations instead of runtime schema creation.

## Run (development)

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Notable security and behavior changes made
- `config.py` now requires `DATABASE_URL` and `SECRET_KEY` from the environment and will fail fast if missing.
- CORS is configurable via `ALLOWED_ORIGINS` and `ALLOW_CREDENTIALS` environment variables.
- Uploads are streamed to disk with a configurable `MAX_UPLOAD_SIZE` (default 10MB). Filenames are replaced by UUIDs.
- Transcription model (`whisper`) is lazy-loaded and errors are handled to avoid crashing startup.
- Login now has a simple in-memory rate limiter (per username+IP). Replace with Redis for production.
- Endpoints that return lists (`/users`, `/sessions`) now return safe fields and do not expose `password_hash` or file paths.
- Better error handling and logging in critical paths.

## Next recommended improvements
- Add Alembic for DB migrations and remove runtime `create_all`.
	- To initialize migrations locally:

```bash
pip install -r requirements.txt
# from repository root
alembic upgrade head
```

The Alembic environment is configured with `script_location = backend/alembic`. If `DATABASE_URL` is not present in the environment, set it before running migrations. The initial migration file is available at `backend/alembic/versions/0001_initial.py`.
- Use Redis or another persistent store for rate-limiting and sessions.
- Add tests and CI (GitHub Actions).
- Add virus scanning for uploaded files and content-type validation.

## License
This project has no license file in the repository. Add a license if sharing publicly.
