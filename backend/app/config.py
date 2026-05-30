from dotenv import load_dotenv
import os

load_dotenv()

# We default to a standard local postgres string if not provided in .env
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:admin@localhost:5432/speech-ai")

# Secret key for JWT token generation
SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-it-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
