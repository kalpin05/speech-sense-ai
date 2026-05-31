from dotenv import load_dotenv
import os
import sys

load_dotenv()

# Require DATABASE_URL and SECRET_KEY to be provided via environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
	raise RuntimeError("DATABASE_URL environment variable is required")

# Secret key for JWT token generation
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
	raise RuntimeError("SECRET_KEY environment variable is required")

ALGORITHM = "HS256"
try:
	ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
except ValueError:
	ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Whether to run Base.metadata.create_all on startup. Default false for safety.
ALLOW_CREATE_ALL = os.getenv("ALLOW_CREATE_ALL", "false").lower() in ("1", "true", "yes")
