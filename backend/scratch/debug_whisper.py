import whisper
import os
import wave

wav_path = os.path.dirname(os.path.abspath(__file__)) + "/test_whisper.wav"

with wave.open(wav_path, "rb") as f:
    print(f"File: {wav_path}")
    print(f"Channels: {f.getnchannels()}")
    print(f"Sample Width: {f.getsampwidth()}")
    print(f"Framerate: {f.getframerate()}")
    print(f"Frames: {f.getnframes()}")
    print(f"Duration: {f.getnframes() / f.getframerate():.2f}s")

for model_name in ["base", "turbo"]:
    print(f"\n--- Loading model: {model_name} ---")
    model = whisper.load_model(model_name)
    print("Transcribing...")
    result = model.transcribe(wav_path, language="en", task="transcribe")
    print(f"Result text: '{result.get('text')}'")
