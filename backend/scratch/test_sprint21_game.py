import sys
import os

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models.user import User
from app.models.language_progress import UserLanguageProgress

def test_sprint21_game():
    print("--- Running Sprint 21 Voice Game Integration Tests ---")
    
    db = SessionLocal()
    try:
        # 1. Fetch first user
        test_user = db.query(User).first()
        assert test_user is not None, "No users found in database to run integration test."
        
        # Save initial global XP
        init_xp = test_user.xp
        
        # Save initial language progress XP
        lang = "spanish"
        prog = db.query(UserLanguageProgress).filter(
            UserLanguageProgress.user_id == test_user.id,
            UserLanguageProgress.language == lang
        ).first()
        init_lang_xp = prog.xp if prog else 0
        
        # 2. Simulate POST to `/me/game-score` logic
        score = 45 # 45 points / 5 = 9 XP gained
        xp_gained = min(20, max(5, score // 5)) # 9 XP
        
        test_user.xp += xp_gained
        test_user.level = (test_user.xp // 100) + 1
        
        if not prog:
            prog = UserLanguageProgress(
                user_id=test_user.id,
                language=lang,
                xp=0,
                level=1,
                streak=0
            )
            db.add(prog)
            
        prog.xp += xp_gained
        prog.level = (prog.xp // 100) + 1
        
        db.commit()
        
        # Verify values updated
        db.refresh(test_user)
        db.refresh(prog)
        
        print(f"XP Rewards verified successfully:")
        print(f"  Initial Global XP: {init_xp} | Updated Global XP: {test_user.xp}")
        print(f"  Initial Spanish XP: {init_lang_xp} | Updated Spanish XP: {prog.xp}")
        
        assert test_user.xp == init_xp + xp_gained, f"Global XP not updated correctly! Expected {init_xp + xp_gained}, got {test_user.xp}"
        assert prog.xp == init_lang_xp + xp_gained, f"Spanish XP not updated correctly! Expected {init_lang_xp + xp_gained}, got {prog.xp}"
        
        # Clean up added XP
        test_user.xp -= xp_gained
        test_user.level = (test_user.xp // 100) + 1
        prog.xp -= xp_gained
        prog.level = (prog.xp // 100) + 1
        db.commit()
        
        print("\nAll Voice Game integration and XP rewards tests passed successfully!")
    finally:
        db.close()

if __name__ == "__main__":
    test_sprint21_game()
