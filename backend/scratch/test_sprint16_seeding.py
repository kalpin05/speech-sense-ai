import requests
import time

base_url = "http://127.0.0.1:8000"

def test_sprint16_seeding():
    print("--- Test Sprint 16 Multilingual Seeding ---")
    
    # Wait for startup to complete (seeding occurs on startup)
    time.sleep(2)
    
    # 1. Fetch Spanish Exercises
    print("1. Fetching Spanish exercises...")
    r = requests.get(f"{base_url}/exercises?language=spanish")
    assert r.status_code == 200, f"Failed to fetch Spanish exercises: {r.text}"
    exercises_es = r.json()["exercises"]
    print(f"   Fetched {len(exercises_es)} Spanish exercises.")
    assert "Tres tristes tigres tragaban trigo en un trigal." in exercises_es, "Missing Spanish tongue-twister!"
    print("Success: Spanish tongue-twisters are seeded.")
    
    # 2. Fetch Hindi Exercises
    print("2. Fetching Hindi exercises...")
    r = requests.get(f"{base_url}/exercises?language=hindi")
    assert r.status_code == 200, f"Failed to fetch Hindi exercises: {r.text}"
    exercises_hi = r.json()["exercises"]
    print(f"   Fetched {len(exercises_hi)} Hindi exercises.")
    assert "खड़क सिंह के खड़कने से खड़कती हैं खिड़कियाँ।" in exercises_hi, "Missing Hindi tongue-twister!"
    print("Success: Hindi tongue-twisters are seeded.")
    
    print("\nAll Sprint 16 multilingual database seeding tests passed successfully!")

if __name__ == "__main__":
    try:
        test_sprint16_seeding()
    except requests.exceptions.ConnectionError:
        print("\n[ERROR] Connection refused. Please ensure uvicorn server is running on port 8000!")
