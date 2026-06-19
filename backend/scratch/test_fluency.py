import os
import sys
import numpy as np
from scipy.io import wavfile

# Add app to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.analysis_service import calculate_real_fluency

def generate_test_audio(path):
    # 22050 Hz sampling rate
    sr = 22050
    # Generate 5 seconds of audio:
    # 2 seconds of sound (440Hz sine wave), 1 second of silence, 2 seconds of sound
    t1 = np.linspace(0, 2, 2 * sr, endpoint=False)
    sound1 = np.sin(2 * np.pi * 440 * t1)
    
    silence = np.zeros(1 * sr)
    
    t2 = np.linspace(0, 2, 2 * sr, endpoint=False)
    sound2 = np.sin(2 * np.pi * 440 * t2)
    
    y = np.concatenate([sound1, silence, sound2])
    
    # Scale to 16-bit PCM
    y_scaled = np.int16(y / np.max(np.abs(y)) * 32767)
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    wavfile.write(path, sr, y_scaled)
    print(f"Generated test audio at {path}")

def test_fluency():
    audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_fluency.wav")
    try:
        generate_test_audio(audio_path)
        
        # Expecting around 1 pause (the 1-second silence in the middle)
        transcription = "this is a test sentence with some words to read"
        result = calculate_real_fluency(audio_path, transcription, "en")
        
        print("Fluency calculation result:")
        print(result)
        
        assert isinstance(result, dict), "Result must be a dictionary"
        assert "fluency_score" in result, "Result must contain fluency_score"
        assert "speech_rate" in result, "Result must contain speech_rate"
        assert "pause_count" in result, "Result must contain pause_count"
        assert "category" in result, "Result must contain category"
        
        print("ALL TESTS PASSED SUCCESSFULLY!")
        
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

if __name__ == "__main__":
    test_fluency()
