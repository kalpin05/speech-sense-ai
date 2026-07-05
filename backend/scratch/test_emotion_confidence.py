import sys
import os
import requests
import json
import random

# Add the backend dir to sys.path so we can import app modules directly for unit tests
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from app.services.analysis_service import calculate_acoustic_features, detect_emotion_and_confidence

base_url = "http://127.0.0.1:8000"
wav_path = os.path.dirname(os.path.abspath(__file__)) + "/test_whisper.wav"

def test_vocal_analysis_service():
    print("--- Test Acoustic Feature Extraction & Emotion Analysis Service ---")
    
    # 1. Test feature extraction
    print(f"Loading wav file for acoustic feature check: {wav_path}")
    assert os.path.exists(wav_path), f"Sample audio file {wav_path} not found!"
    
    acoustics = calculate_acoustic_features(wav_path)
    print("Acoustic features computed:")
    print(json.dumps(acoustics, indent=2))
    
    assert "mean_energy" in acoustics
    assert "mean_pitch" in acoustics
    assert acoustics["mean_energy"] >= 0.0
    
    # 2. Test rule-based emotion & confidence classifications
    # Case A: Happy/positive statement
    res_happy = detect_emotion_and_confidence(wav_path, "I am so happy and excited today! This is amazing.", "en")
    print("\nResult for positive text:", res_happy)
    assert res_happy["confidence_score"] >= 0 and res_happy["confidence_score"] <= 100
    assert res_happy["emotion"] in ["happy", "neutral", "sad", "angry", "anxious"]
    
    # Case B: Anxious/negative statement
    res_anxious = detect_emotion_and_confidence(wav_path, "I feel so sad and scared and anxious about this.", "en")
    print("Result for negative/anxious text:", res_anxious)
    assert res_anxious["nervousness_score"] >= 0 and res_anxious["nervousness_score"] <= 100
    
    # Case C: Spanish checks
    res_es = detect_emotion_and_confidence(wav_path, "Hola, este... bueno... estoy un poco cansado.", "es")
    print("Result for Spanish filler text:", res_es)
    assert res_es["hesitation_score"] > 0, "Filler count should trigger hesitation penalty"

    print("Offline analysis service tests passed successfully!\n")

def test_api_integration():
    print("--- Test API Endpoints for Emotion & Confidence ---")
    
    # Generate unique credentials to avoid registration conflict
    rand_num = random.randint(1000, 9999)
    email = f"sprint11_user_{rand_num}@example.com"
    password = "password123"
    
    # 1. Register User
    print("1. Registering user...")
    register_data = {
        "email": email,
        "password": password,
        "first_name": "Sprint11",
        "last_name": "Test"
    }
    r = requests.post(f"{base_url}/auth/register", json=register_data)
    assert r.status_code == 201 or r.status_code == 200, f"Registration failed: {r.text}"

    # 2. Login User
    print("2. Logging in...")
    login_data = {
        "username": email,
        "password": password
    }
    r = requests.post(f"{base_url}/auth/login", data=login_data)
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}

    # 3. Post audio for analysis (expected: Happy sentiment text)
    print("3. Uploading audio to /analyze with happy transcript...")
    with open(wav_path, "rb") as audio_file:
        files = {"file": (os.path.basename(wav_path), audio_file, "audio/wav")}
        data = {
            "expected_text": "The quick brown fox jumps over the lazy dog.",
            "language": "English"
        }
        r = requests.post(f"{base_url}/analyze", files=files, data=data, headers=headers)
        
    assert r.status_code == 200, f"Analysis endpoint failed: {r.text}"
    res_analyze = r.json()
    print("   /analyze response received successfully.")

    # 4. Check user analytics (averages and emotion breakdown should be calculated)
    print("4. Fetching user analytics...")
    r = requests.get(f"{base_url}/users/me/analytics", headers=headers)
    assert r.status_code == 200, f"GET /users/me/analytics failed: {r.text}"
    analytics = r.json()
    
    print("\nAnalytics payload:")
    print(json.dumps(analytics, indent=2))
    
    assert "average_confidence" in analytics
    assert "average_nervousness" in analytics
    assert "average_hesitation" in analytics
    assert "emotion_breakdown" in analytics
    assert analytics["total_attempts"] == 1
    
    session = analytics["sessions"][0]
    assert "confidence_score" in session
    assert "nervousness_score" in session
    assert "hesitation_score" in session
    assert "emotion" in session
    print(f"   Session metrics: Emotion={session['emotion']}, Confidence={session['confidence_score']}%")

    print("\nAPI Integration checks passed successfully!")

if __name__ == "__main__":
    test_vocal_analysis_service()
    try:
        test_api_integration()
    except requests.exceptions.ConnectionError:
        print("\n[WARNING] Could not connect to API server at http://127.0.0.1:8000.")
        print("Please ensure the FastAPI dev server is running on port 8000, then run this test again.")
        sys.exit(1)
    print("\nAll integration tests for Sprint 11 completed successfully!")
