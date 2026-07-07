import threading

_model = None
_model_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                try:
                    import whisper
                    _model = whisper.load_model("base")
                except Exception as e:
                    raise RuntimeError("Failed to load transcription model") from e
    return _model


def transcribe_audio(file_path: str, language_code: str):
    model = _get_model()
    result = model.transcribe(
        file_path,
        language=language_code,   # 🔥 FORCE LANGUAGE
        task="transcribe"
    )

    return result.get("text", "").strip()


def transcribe_audio_detailed(file_path: str, language_code: str) -> dict:
    model = _get_model()
    result = model.transcribe(
        file_path,
        language=language_code,
        task="transcribe",
        word_timestamps=True
    )
    return result