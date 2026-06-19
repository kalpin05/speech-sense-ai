import os
import sys
import numpy as np
from scipy.io import wavfile

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.whisper_service import _get_model

def generate_test_audio(path):
    sr = 16000
    t = np.linspace(0, 1.5, int(1.5 * sr), endpoint=False)
    y = np.sin(2 * np.pi * 440 * t)
    y_scaled = np.int16(y / np.max(np.abs(y)) * 32767)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, sr, y_scaled)

def test_whisper_timestamps():
    audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_whisper.wav")
    try:
        generate_test_audio(audio_path)
        print("Loading Whisper model...")
        model = _get_model()
        print("Transcribing with word timestamps...")
        result = model.transcribe(audio_path, word_timestamps=True, language="en")
        print("Transcription complete. Output segments:")
        for segment in result.get("segments", []):
            print(f"Segment: {segment.get('text')}")
            print(f"Words: {segment.get('words')}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    test_whisper_timestamps()
