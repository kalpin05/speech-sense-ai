import threading
import os
import logging

log = logging.getLogger(__name__)

_model = None
_model_lock = threading.Lock()


def _get_model():
    global _model
    if _model is None:
        with _model_lock:
            if _model is None:
                try:
                    import whisper
                    model_name = os.getenv("WHISPER_MODEL_NAME", "base")
                    log.info(f"Loading Whisper model '{model_name}'...")
                    _model = whisper.load_model(model_name)
                except Exception as e:
                    log.exception("Failed to load Whisper model")
                    raise RuntimeError("Failed to load transcription model") from e
    return _model


def preload_model():
    log.info("Preloading Whisper transcription model...")
    _get_model()
    log.info("Whisper model successfully preloaded into memory!")


def transcribe_audio(file_path: str, language_code: str):
    model = _get_model()
    result = model.transcribe(
        file_path,
        language=language_code,   # 🔥 FORCE LANGUAGE
        task="transcribe",
        fp16=False                # CPU-safe: disable half-precision float
    )

    return result.get("text", "").strip()


def transcribe_audio_detailed(file_path: str, language_code: str) -> dict:
    model = _get_model()
    result = model.transcribe(
        file_path,
        language=language_code,
        task="transcribe",
        word_timestamps=True,
        fp16=False                # CPU-safe: disable half-precision float
    )
    return result