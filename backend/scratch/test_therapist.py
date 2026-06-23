import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.models.session_model import TherapySession
from app.services.auth_service import get_password_hash

def run_integration_test():
    db = SessionLocal()
    
    # 1. Clean up existing test users if they exist
    db.query(User).filter(User.email.in_(["test_patient@example.com", "test_therapist@example.com"])).delete(synchronize_session=False)
    db.commit()
    
    # 2. Create test users
    therapist_pwd = get_password_hash("password123")
    therapist = User(
        email="test_therapist@example.com",
        password_hash=therapist_pwd,
        first_name="Dr.",
        last_name="Smith",
        role="therapist"
    )
    
    patient_pwd = get_password_hash("password123")
    patient = User(
        email="test_patient@example.com",
        password_hash=patient_pwd,
        first_name="John",
        last_name="Doe",
        role="patient"
    )
    
    db.add(therapist)
    db.add(patient)
    db.commit()
    db.refresh(therapist)
    db.refresh(patient)
    
    print(f"Created test therapist: {therapist.email} (id: {therapist.id})")
    print(f"Created test patient: {patient.email} (id: {patient.id})")
    
    # Assert initial roles
    assert therapist.role == "therapist"
    assert patient.role == "patient"
    assert patient.therapist_id is None
    
    # 3. Simulate Linkage API (Putting email of therapist)
    # Check link validation
    target_therapist = db.query(User).filter(User.email == "test_therapist@example.com").first()
    assert target_therapist is not None
    assert target_therapist.role == "therapist"
    
    patient.therapist_id = target_therapist.id
    db.commit()
    db.refresh(patient)
    
    print(f"Linked patient {patient.email} to therapist {target_therapist.email}")
    assert patient.therapist_id == target_therapist.id
    
    # 4. Simulate therapist querying linked patients
    linked_patients = db.query(User).filter(User.therapist_id == therapist.id, User.role == "patient").all()
    print(f"Therapist {therapist.email} has {len(linked_patients)} linked patients")
    assert len(linked_patients) == 1
    assert linked_patients[0].id == patient.id
    
    # 5. Create a mock session for the patient
    session = TherapySession(
        user_id=patient.id,
        expected_text="Hello how are you",
        transcription="Hello how you",
        language="english",
        accuracy_score=75.0,
        fluency_score="medium",
        fluency_score_val=70,
        speech_rate=120,
        pause_count=1,
        feedback=json.dumps({
            "message": "Good!",
            "incorrect_words": ["are"],
            "detailed_analysis": []
        })
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    print(f"Created mock session for patient John Doe: {session.expected_text}")
    
    # Query sessions as therapist
    patient_sessions = db.query(TherapySession).filter(TherapySession.user_id == patient.id).all()
    assert len(patient_sessions) == 1
    assert "are" in json.loads(patient_sessions[0].feedback)["incorrect_words"]
    print("Therapist queried patient session successfully.")
    
    # 6. Simulate Unlink API
    patient.therapist_id = None
    db.commit()
    db.refresh(patient)
    print("Unlinked patient from therapist.")
    assert patient.therapist_id is None
    
    # Clean up test users
    db.query(User).filter(User.email.in_(["test_patient@example.com", "test_therapist@example.com"])).delete(synchronize_session=False)
    db.commit()
    db.close()
    print("All integration assertions passed successfully!")

if __name__ == "__main__":
    run_integration_test()
