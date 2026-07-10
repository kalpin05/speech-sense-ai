import sys
import os

# Add paths like in env.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT_DIR)

try:
    from app.database import Base
    from app.config import DATABASE_URL
    from app.models.user import User
    from app.models.session_model import TherapySession
    from app.models.settings_model import UserSettings
    from app.models.badge_model import UserBadge
    from app.models.exercise_model import Exercise
    from app.models.language_progress import UserLanguageProgress
    print("SUCCESS: Imported all models successfully!")
except Exception as e:
    import traceback
    print("ERROR occurred:")
    traceback.print_exc()
