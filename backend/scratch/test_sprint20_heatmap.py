import sys
import os
from datetime import datetime, timedelta

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User
from app.models.session_model import TherapySession

def test_sprint20_heatmap():
    print("--- Running Sprint 20 Practice Consistency Heatmap Tests ---")
    
    db = SessionLocal()
    try:
        # 1. Fetch any test user
        test_user = db.query(User).first()
        if not test_user:
            print("No users found in database to run integration test. Creating mock user...")
            test_user = User(email="heatmap@test.com", hashed_password="mock", is_active=True)
            db.add(test_user)
            db.commit()
            db.refresh(test_user)
            
        # 2. Add mock sessions for yesterday and today
        today = datetime.utcnow()
        yesterday = today - timedelta(days=1)
        
        session_today1 = TherapySession(
            user_id=test_user.id,
            expected_text="Hello",
            transcription="Hello",
            language="english",
            accuracy_score=100.0,
            fluency_score="Good",
            feedback="{}",
            created_at=today
        )
        session_today2 = TherapySession(
            user_id=test_user.id,
            expected_text="World",
            transcription="World",
            language="english",
            accuracy_score=95.0,
            fluency_score="Good",
            feedback="{}",
            created_at=today
        )
        session_yesterday = TherapySession(
            user_id=test_user.id,
            expected_text="Yesterday",
            transcription="Yesterday",
            language="english",
            accuracy_score=80.0,
            fluency_score="Good",
            feedback="{}",
            created_at=yesterday
        )
        
        db.add_all([session_today1, session_today2, session_yesterday])
        db.commit()
        
        # 3. Simulate group_by logic
        from sqlalchemy import func
        start_date = datetime.utcnow() - timedelta(days=180)
        
        results = db.query(
            func.date(TherapySession.created_at).label("date"),
            func.count(TherapySession.id).label("count")
        ).filter(
            TherapySession.user_id == test_user.id,
            TherapySession.created_at >= start_date
        ).group_by(
            func.date(TherapySession.created_at)
        ).all()
        
        heatmap_data = {str(r.date): r.count for r in results}
        
        print("Heatmap dictionary generated:")
        for date_str, count in heatmap_data.items():
            print(f"  Date: {date_str} | Session Count: {count}")
            
        # Assertions
        today_date_str = str(today.date())
        yesterday_date_str = str(yesterday.date())
        
        assert heatmap_data.get(today_date_str, 0) >= 2, f"Expected at least 2 sessions today, got {heatmap_data.get(today_date_str)}"
        assert heatmap_data.get(yesterday_date_str, 0) >= 1, f"Expected at least 1 session yesterday, got {heatmap_data.get(yesterday_date_str)}"
        
        # Clean up mock sessions
        db.delete(session_today1)
        db.delete(session_today2)
        db.delete(session_yesterday)
        db.commit()
        
        print("\nAll heatmap SQL groupings and data integration tests passed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    test_sprint20_heatmap()
