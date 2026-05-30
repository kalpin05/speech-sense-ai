import os


def is_valid_audio(filename: str) -> bool:
    return filename.endswith((".wav", ".mp3", ".m4a"))