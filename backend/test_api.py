import requests
import json

base_url = "http://127.0.0.1:8000"

print("1. Testing GET /health")
r = requests.get(f"{base_url}/health")
print(r.status_code, r.text)

print("\n2. Testing GET /exercises")
r = requests.get(f"{base_url}/exercises?language=english")
print(r.status_code, r.text)

print("\n3. Registering User")
register_data = {
    "email": "test@example.com",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User"
}
r = requests.post(f"{base_url}/auth/register", json=register_data)
print(r.status_code, r.text)

print("\n4. Login User")
login_data = {
    "username": "test@example.com",
    "password": "password123"
}
r = requests.post(f"{base_url}/auth/login", data=login_data)
print(r.status_code, r.text)
if r.status_code == 200:
    token = r.json().get("access_token")
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n5. GET /auth/me")
    r = requests.get(f"{base_url}/auth/me", headers=headers)
    print(r.status_code, r.text)
    
    print("\n6. GET /users/me/sessions")
    r = requests.get(f"{base_url}/users/me/sessions", headers=headers)
    print(r.status_code, r.text)
