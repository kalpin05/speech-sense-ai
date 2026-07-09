# Speech Therapy Platform 🎯

An intelligent, multi-lingual speech therapy platform with adaptive exercises, AI-powered feedback, gamified achievements, patient analytics, therapist oversight, vocal emotion/confidence tracking, and a real-time speech room utilizing WebSockets.

---

## 🚀 Quick Start (Recommended: Docker Setup)

The easiest way to run the entire stack (FastAPI Backend, PostgreSQL Database, and Frontend assets) is using **Docker Compose**.

### Prerequisites
* Install **Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop/)

### 1. Clone & Set Up Configuration
Ensure you have the project folder on your machine. In the root directory, create a `.env` file to configure your environment variables:

```env
# Root .env configuration (Optional but recommended for AI features)
OPENAI_API_KEY=your-openai-api-key-here
MAX_UPLOAD_SIZE=10485760
WHISPER_MODEL_NAME=base
```

### 2. Start the Application
Open a terminal in the project root directory and run:

* **First-time run (Builds image and starts database + web server)**:
  ```bash
  docker compose up --build -d
  ```
* **Subsequent runs (Starts the project instantly in 1-2 seconds)**:
  ```bash
  docker compose up -d
  ```

Docker Compose will automatically:
1. Initialize the PostgreSQL 15 container.
2. Build the web app, installing all requirements (including Whisper, PyTorch, Librosa).
3. Automatically wait for the database port and execute **Alembic database migrations**.
4. Pre-load the Whisper transcription model in the background.

### 3. Access the Application
Open your browser and navigate to:
👉 **[http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html)**

### 4. Stop the Application
To stop all running container services safely:
```bash
docker compose down
```

---

## 🛠️ Alternative: Local Development Setup (Manual)

If you prefer to run the application directly on your host machine without Docker:

### 1. Set Up Python Environment
Create a Python virtual environment (Python 3.10+ recommended) and install dependencies:

```bash
# In the repository root
python -m venv backend/venv
# Windows:
.\backend\venv\Scripts\activate
# macOS/Linux:
source backend/venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Configure Local PostgreSQL Database
1. Install PostgreSQL locally.
2. Create a database named `speech-ai`.
3. Set your environment variables:
   ```env
   DATABASE_URL=postgresql://<username>:<password>@localhost:5432/speech-ai
   SECRET_KEY=change-me-to-a-secret-value
   WHISPER_MODEL_NAME=base
   ```

### 3. Run Database Migrations
Run the Alembic migrations to construct the database schema:
```bash
alembic upgrade head
```

### 4. Start the Backend Server
Start the FastAPI server:
```bash
# Windows / macOS / Linux
uvicorn app.main:app --host 127.0.0.1 --port 8000
```
Open [http://127.0.0.1:8000/index.html](http://127.0.0.1:8000/index.html) in your browser.

---

## ⚡ Main Features & Architecture

* **Speech recognition & Pronunciation accuracy**: Driven by OpenAI Whisper (CPU-optimized `base` model) and Levenshtein alignment calculations.
* **Fluency Analytics**: Computes real fluency stats, speech rate (WPM), and silence pauses using `librosa`.
* **Acoustics & Emotion Core**: Evaluates pitch jitter and volume stability to measure confidence, nervousness, and hesitation, along with local rule-based and GPT sentiment models to detect emotional tone (Happy, Sad, Anxious, Angry, Neutral).
* **Live WebSockets room**: A real-time speech therapy simulator with HTML5 microphone PCM streaming and instant word-by-word highlights (Green/Red feedback).
* **Gamification system**: XP and level progression with unlockable achievements (e.g. First Steps, Accuracy Champ, Consistent Learner, Multi-lingual).
* **Therapist Portal**: Allows linked therapists to inspect patient attempt histories, aggregates, adaptive weak-sound analyses, and badges.
* **Dockerized Setup**: Secure, isolated multi-container configuration for smooth production releases.
