import sys
import os
import json

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

# Create a mock database session
class MockUser:
    def __init__(self, id):
        self.id = id

class MockTherapySession:
    def __init__(self, user_id, expected_text, language, feedback):
        self.user_id = user_id
        self.expected_text = expected_text
        self.language = language
        self.feedback = feedback
        self.created_at = None

class MockQuery:
    def __init__(self, items):
        self.items = items
        self._filters = []
        self._orders = []
        self._limit = None

    def filter(self, *args, **kwargs):
        return self

    def order_by(self, *args):
        return self

    def limit(self, l):
        self._limit = l
        return self

    def all(self):
        if self._limit:
            return self.items[:self._limit]
        return self.items

class MockDb:
    def __init__(self, sessions):
        self.sessions = sessions

    def query(self, model):
        return MockQuery(self.sessions)

# Import the get_adaptive_exercises logic (or copy it here for isolated logic testing, but importing is better)
# Wait, we can test it by calling it directly.
from app.main import get_adaptive_exercises, get_exercises

def test_adaptive_exercises():
    # Setup mock user and sessions
    user = MockUser(id="user-123")
    
    # 3 sessions with errors
    sessions = [
        MockTherapySession(
            user_id="user-123",
            expected_text="The quick brown fox jumps over the lazy dog.",
            language="english",
            feedback=json.dumps({
                "incorrect_words": ["quick", "fox"],
                "detailed_analysis": []
            })
        ),
        MockTherapySession(
            user_id="user-123",
            expected_text="Technology is evolving at an unprecedented pace.",
            language="english",
            feedback=json.dumps({
                "incorrect_words": ["technology", "unprecedented", "pace"],
                "detailed_analysis": []
            })
        ),
        MockTherapySession(
            user_id="user-123",
            expected_text="Pneumonoultramicroscopicslicovolcanoconiosis is a long word.",
            language="english",
            feedback=json.dumps({
                "incorrect_words": ["technology", "quick"], # repeating mistakes
                "detailed_analysis": []
            })
        )
    ]
    
    db = MockDb(sessions)
    
    # Call get_adaptive_exercises
    res = get_adaptive_exercises(language="english", db=db, current_user=user)
    print("Adaptive Recommendations Result:")
    print(json.dumps(res, indent=2))
    
    # Assertions
    # Weak words should be: technology (2 errors), quick (2 errors), fox (1), unprecedented (1), pace (1)
    assert len(res["weak_words"]) > 0
    assert res["weak_words"][0] in ["technology", "quick"]
    
    # Weak sounds should capture prefix clusters (e.g. "th", "sh", "ch", etc.)
    # "technology" starts with "t", but our patterns don't have "t" alone. Wait, "tr" is there. 
    # "quick" starts with nothing in patterns (no "q"). "fox" starts with "f". 
    # "unprecedented" starts with nothing. "pace" starts with nothing (no "p"). 
    # Let's verify what sounds are extracted
    print("Extracted weak sounds:", res["weak_sounds"])
    
    # Recommended exercises should contain the weak words:
    # "technology" should recommend "Technology is evolving..."
    # "quick" should recommend "The quick brown fox..."
    print("Recommended Exercises:")
    for ex in res["recommended_exercises"]:
        print("-", ex)
        
    assert any("quick" in ex.lower() for ex in res["recommended_exercises"])
    assert any("technology" in ex.lower() for ex in res["recommended_exercises"])

    print("\n--- Test Exercise Filtering ---")
    # Test difficulty filters
    all_ex = get_exercises(language="english")
    beginner_ex = get_exercises(language="english", difficulty="beginner")
    intermediate_ex = get_exercises(language="english", difficulty="intermediate")
    advanced_ex = get_exercises(language="english", difficulty="advanced")
    
    print(f"Total exercises: {len(all_ex['exercises'])}")
    print(f"Beginner exercises: {len(beginner_ex['exercises'])}")
    print(f"Intermediate exercises: {len(intermediate_ex['exercises'])}")
    print(f"Advanced exercises: {len(advanced_ex['exercises'])}")
    
    assert len(all_ex["exercises"]) == len(beginner_ex["exercises"]) + len(intermediate_ex["exercises"]) + len(advanced_ex["exercises"])
    assert len(beginner_ex["exercises"]) > 0
    assert len(advanced_ex["exercises"]) > 0

    print("\nAll Sprint 6 adaptive logic tests passed successfully!")

if __name__ == "__main__":
    test_adaptive_exercises()
