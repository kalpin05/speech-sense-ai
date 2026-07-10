import requests
import uuid
import os

base_url = "http://127.0.0.1:8000"

def test_sprint17_per_language():
    print("--- Test Sprint 17 Per-Language Progress & Gamification ---")
    
    # Generate unique credentials
    username = f"user_{uuid.uuid4().hex}"
    email = f"{username}@example.com"
    password = "SecurePassword123"
    
    # 1. Register
    print("1. Registering test user...")
    r = requests.post(f"{base_url}/auth/register", json={
        "email": email,
        "password": password,
        "first_name": "ProgressTest",
        "last_name": "User",
        "role": "patient"
    })
    assert r.status_code == 200, f"Registration failed: {r.text}"
    
    # 2. Login
    print("2. Logging in...")
    r = requests.post(f"{base_url}/auth/login", data={
        "username": email,
        "password": password
    })
    assert r.status_code == 200, f"Login failed: {r.text}"
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Check Initial Gamification for Spanish and English
    print("3. Checking initial gamification status...")
    r = requests.get(f"{base_url}/users/me/gamification?language=spanish", headers=headers)
    assert r.status_code == 200, f"Failed to get Spanish gamification: {r.text}"
    gam_es = r.json()
    assert gam_es["xp"] == 0, f"Expected 0 initial XP, got {gam_es['xp']}"
    
    r = requests.get(f"{base_url}/users/me/gamification?language=english", headers=headers)
    assert r.status_code == 200, f"Failed to get English gamification: {r.text}"
    gam_en = r.json()
    assert gam_en["xp"] == 0, f"Expected 0 initial XP, got {gam_en['xp']}"
    
    # 4. Upload Spanish Session
    print("4. Uploading Spanish therapy session...")
    wav_path = os.path.dirname(os.path.abspath(__file__)) + "/test_whisper.wav"
    assert os.path.exists(wav_path), f"Test audio {wav_path} not found!"
    
    payload = {
        "expected_text": "hello",
        "language": "Spanish"
    }
    with open(wav_path, "rb") as f:
        files = {"file": ("test_whisper.wav", f, "audio/wav")}
        r = requests.post(f"{base_url}/analyze", data=payload, files=files, headers=headers)
    assert r.status_code == 200, f"Upload failed: {r.text}"
    print("   Spanish session saved successfully.")
    
    # 5. Check Gamification again (Spanish should increase, English should stay 0)
    print("5. Checking progress isolation...")
    r = requests.get(f"{base_url}/users/me/gamification?language=spanish", headers=headers)
    gam_es_after = r.json()
    print(f"   Spanish XP after: {gam_es_after['xp']}, Level: {gam_es_after['level']}")
    assert gam_es_after["xp"] == 10, f"Expected 10 XP in Spanish, got {gam_es_after['xp']}"
    
    r = requests.get(f"{base_url}/users/me/gamification?language=english", headers=headers)
    gam_en_after = r.json()
    print(f"   English XP after: {gam_en_after['xp']}")
    assert gam_en_after["xp"] == 0, f"Expected 0 XP in English, got {gam_en_after['xp']}"
    
    # 6. Check Analytics isolation
    print("6. Checking analytics isolation...")
    r = requests.get(f"{base_url}/users/me/analytics?language=spanish", headers=headers)
    assert r.status_code == 200
    ana_es = r.json()
    assert ana_es["total_attempts"] == 1, f"Expected 1 Spanish attempt, got {ana_es['total_attempts']}"
    
    r = requests.get(f"{base_url}/users/me/analytics?language=english", headers=headers)
    assert r.status_code == 200
    ana_en = r.json()
    assert ana_en["total_attempts"] == 0, f"Expected 0 English attempts, got {ana_en['total_attempts']}"
    
    print("\nAll Sprint 17 per-language isolation checks passed successfully!")

if __name__ == "__main__":
    try:
        test_sprint17_per_language()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection refused. Please ensure uvicorn server is running on port 8000!")
