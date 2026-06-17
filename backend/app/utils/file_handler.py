import os
from pathlib import Path


def is_valid_audio(filename: str) -> bool:
    return Path(filename).suffix.lower() in (".wav", ".mp3", ".m4a", ".mp4", ".webm", ".ogg")


def sanitize_extension(filename: str) -> str:
    """Return a safe extension (including leading dot) or empty string if not allowed."""
    ext = Path(filename).suffix.lower()
    return ext if ext in (".wav", ".mp3", ".m4a", ".mp4", ".webm", ".ogg") else ""