import sys
import os

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.analysis_service import analyze_pronunciation

def test_sprint19_diff():
    print("--- Running Sprint 19 Pronunciation Diff Tests ---")
    
    # 1. Test standard case where no detailed segments exist (simple diff fallback)
    whisper_fallback = {"text": "hello how is you"}
    result_fallback = analyze_pronunciation("hello how are you", whisper_fallback)
    
    analysis_fallback = result_fallback["detailed_analysis"]
    print("1. Fallback matching result:")
    for item in analysis_fallback:
        print(f"  Word: {item['word']} | Status: {item['status']} | Heard: {item['heard']}")
        if item['word'] == "are":
            assert item['status'] == "incorrect"
            assert item['heard'] == "unknown"
            
    # 2. Test alignment case where segment word objects exist
    whisper_aligned = {
        "text": "the quick brown fox",
        "segments": [{
            "words": [
                {"word": "the", "start": 0.1, "end": 0.3, "probability": 0.99},
                {"word": "kwick", "start": 0.4, "end": 0.8, "probability": 0.85},
                {"word": "brown", "start": 0.9, "end": 1.3, "probability": 0.95}
            ]
        }]
    }
    
    result_aligned = analyze_pronunciation("the quick brown fox", whisper_aligned)
    analysis_aligned = result_aligned["detailed_analysis"]
    
    print("\n2. Aligned needleman-wunsch result:")
    for item in analysis_aligned:
        print(f"  Word: {item['word']} | Status: {item['status']} | Error Type: {item['error_type']} | Heard: {item['heard']}")
        if item['word'] == "quick":
            assert item['status'] == "incorrect"
            assert item['heard'] == "kwick"
        elif item['word'] == "fox":
            assert item['status'] == "incorrect"
            assert item['error_type'] == "omitted"
            assert item['heard'] is None
            
    print("\nAll word-by-word pronunciation diff tests passed successfully!")

if __name__ == "__main__":
    test_sprint19_diff()
