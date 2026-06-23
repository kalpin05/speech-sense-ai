from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
import time
import logging
from pydantic import BaseModel

log = logging.getLogger(__name__)

# Simple in-memory rate limiter for login attempts (per username). This is
# intentionally lightweight; replace with Redis or another store for production.
FAILED_LOGIN_ATTEMPTS: dict[str, list[float]] = {}
RATE_LIMIT_WINDOW = int(__import__('os').getenv('LOGIN_RATE_WINDOW', 300))  # seconds
MAX_LOGIN_ATTEMPTS = int(__import__('os').getenv('MAX_LOGIN_ATTEMPTS', 5))

from app.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserResponse, Token
from app.services.auth_service import get_password_hash, verify_password, create_access_token, get_current_user
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()


def _prune_attempts(key: str):
    """Remove expired failed login attempts for a key."""
    now = time.time()
    attempts = FAILED_LOGIN_ATTEMPTS.get(key, [])
    attempts = [t for t in attempts if now - t <= RATE_LIMIT_WINDOW]
    if attempts:
        FAILED_LOGIN_ATTEMPTS[key] = attempts
    else:
        FAILED_LOGIN_ATTEMPTS.pop(key, None)


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(
        email=user.email,
        password_hash=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role if user.role in ("patient", "therapist") else "patient"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    key = form_data.username

    _prune_attempts(key)
    if len(FAILED_LOGIN_ATTEMPTS.get(key, [])) >= MAX_LOGIN_ATTEMPTS:
        log.warning("Too many login attempts for %s", form_data.username)
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts. Try again later.")

    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        FAILED_LOGIN_ATTEMPTS.setdefault(key, []).append(time.time())
        log.info("Failed login for %s", form_data.username)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    FAILED_LOGIN_ATTEMPTS.pop(key, None)
    return {"access_token": access_token, "token_type": "bearer"}


class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login-json", response_model=Token)
def login_json(payload: LoginRequest, db: Session = Depends(get_db)):
    """Accept JSON {username, password} and return token. Useful for non-form clients."""
    key = payload.username

    _prune_attempts(key)
    if len(FAILED_LOGIN_ATTEMPTS.get(key, [])) >= MAX_LOGIN_ATTEMPTS:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Too many login attempts. Try again later.")

    user = db.query(User).filter(User.email == payload.username).first()
    if not user or not verify_password(payload.password, user.password_hash):
        FAILED_LOGIN_ATTEMPTS.setdefault(key, []).append(time.time())
        log.info("Failed login-json for %s", payload.username)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)
    FAILED_LOGIN_ATTEMPTS.pop(key, None)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Fetch the currently logged in user's profile."""
    return current_user
