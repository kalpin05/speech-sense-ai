FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies (ffmpeg and libsndfile1 for audio decoding, build-essential for any C compilation)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY backend/app ./app
COPY alembic.ini ./alembic.ini
COPY backend/alembic ./alembic

# Copy frontend static files to /frontend to match Path(__file__).resolve().parents[2] / "frontend" path in main.py
COPY frontend /frontend

# Expose port
EXPOSE 8000

# Wait for database, run database migrations, then start FastAPI server
CMD ["sh", "-c", "python -c \"import socket, time; [time.sleep(1) for _ in range(30) if socket.socket().connect_ex(('db', 5432)) != 0]\" && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
