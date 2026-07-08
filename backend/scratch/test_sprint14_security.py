import requests
import os
import uuid

base_url = "http://127.0.0.1:8000"

def test_sprint14_security():
    print("--- Test Sprint 14 Security & File Validation ---")
    
    # Generate unique credentials
    username = f"user_{uuid.uuid4().hex}"
    email = f"{username}@example.com"
    password = "SecurePassword123"
    
    # 1. Register
    print("1. Registering test user...")
    r = requests.post(f"{base_url}/auth/register", json={
        "email": email,
        "password": password,
        "first_name": "SecurityTest",
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
    
    # 3. Test Invalid Extension Suffix
    print("3. Testing invalid file extension suffix (.txt)...")
    payload = {
        "expected_text": "Hello world",
        "language": "English"
    }
    files = {"file": ("test.txt", b"dummy content", "audio/wav")}
    r = requests.post(f"{base_url}/analyze", data=payload, files=files, headers=headers)
    print(f"   Response status: {r.status_code}, detail: {r.text}")
    assert r.status_code == 400, "Allowed invalid file extension suffix!"
    
    # 4. Test Invalid MIME type
    print("4. Testing invalid MIME content-type (text/plain on wav)...")
    files = {"file": ("test.wav", b"dummy content", "text/plain")}
    r = requests.post(f"{base_url}/analyze", data=payload, files=files, headers=headers)
    print(f"   Response status: {r.status_code}, detail: {r.text}")
    assert r.status_code == 400, "Allowed invalid MIME type!"
    
    # 5. Test Valid File & MIME type
    print("5. Testing valid file extension and MIME type (audio/wav)...")
    wav_path = os.path.dirname(os.path.abspath(__file__)) + "/test_whisper.wav"
    assert os.path.exists(wav_path), f"Test audio {wav_path} not found!"
    
    with open(wav_path, "rb") as f:
        files = {"file": ("test_whisper.wav", f, "audio/wav")}
        r = requests.post(f"{base_url}/analyze", data=payload, files=files, headers=headers)
        
    print(f"   Response status: {r.status_code}")
    assert r.status_code == 200, f"Valid audio file upload failed: {r.text}"
    print("Success: Valid audio upload accepted.")
    
    print("\nAll Sprint 14 file validation checks passed successfully!")

if __name__ == "__main__":
    try:
        test_sprint14_security()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection refused. Please ensure uvicorn server is running on port 8000!")
