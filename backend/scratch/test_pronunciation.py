import sys
import os

# Add backend directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app.services.analysis_service import align_words_needleman_wunsch, analyze_pronunciation

def test_alignment():
    # Test case 1: exact match
    expected = ["the", "quick", "brown", "fox"]
    transcribed = [
        {"word": "the", "probability": 0.99, "start": 0.0, "end": 0.2},
        {"word": "quick", "probability": 0.98, "start": 0.2, "end": 0.5},
        {"word": "brown", "probability": 0.97, "start": 0.5, "end": 0.8},
        {"word": "fox", "probability": 0.96, "start": 0.8, "end": 1.1},
    ]
    
    alignment = align_words_needleman_wunsch(expected, transcribed)
    print("Alignment exact:", alignment)
    assert alignment == [(0, 0), (1, 1), (2, 2), (3, 3)]
    
    # Test case 2: Omission (brown is omitted)
    transcribed_omitted = [
        {"word": "the", "probability": 0.99, "start": 0.0, "end": 0.2},
        {"word": "quick", "probability": 0.98, "start": 0.2, "end": 0.5},
        {"word": "fox", "probability": 0.96, "start": 0.5, "end": 0.8},
    ]
    alignment_omitted = align_words_needleman_wunsch(expected, transcribed_omitted)
    print("Alignment omitted:", alignment_omitted)
    # Brown (index 2) should map to None
    # the->the (0,0), quick->quick (1,1), brown->None (2, None), fox->fox (3,2)
    assert alignment_omitted == [(0, 0), (1, 1), (2, None), (3, 2)]

    # Test case 3: Mispronunciation / spelling mismatch (quick is pronounced as quack)
    transcribed_mispronounced = [
        {"word": "the", "probability": 0.99, "start": 0.0, "end": 0.2},
        {"word": "quack", "probability": 0.98, "start": 0.2, "end": 0.5},
        {"word": "brown", "probability": 0.97, "start": 0.5, "end": 0.8},
        {"word": "fox", "probability": 0.96, "start": 0.8, "end": 1.1},
    ]
    alignment_mis = align_words_needleman_wunsch(expected, transcribed_mispronounced)
    print("Alignment mispronounced:", alignment_mis)
    assert alignment_mis == [(0, 0), (1, 1), (2, 2), (3, 3)]
    
    # Analyze pronunciation
    whisper_res = {
        "text": "the quack brown fox",
        "segments": [{
            "words": transcribed_mispronounced
        }]
    }
    
    analysis = analyze_pronunciation("the quick brown fox", whisper_res)
    print("Analysis:", analysis)
    assert "quick" in analysis["incorrect_words"]
    
    # Check low confidence
    transcribed_low_conf = [
        {"word": "the", "probability": 0.99, "start": 0.0, "end": 0.2},
        {"word": "quick", "probability": 0.55, "start": 0.2, "end": 0.5}, # low probability
        {"word": "brown", "probability": 0.97, "start": 0.5, "end": 0.8},
        {"word": "fox", "probability": 0.96, "start": 0.8, "end": 1.1},
    ]
    whisper_res_low = {
        "text": "the quick brown fox",
        "segments": [{
            "words": transcribed_low_conf
        }]
    }
    analysis_low = analyze_pronunciation("the quick brown fox", whisper_res_low)
    print("Analysis Low Confidence:", analysis_low)
    assert "quick" in analysis_low["incorrect_words"]
    
    print("All tests passed successfully!")

if __name__ == "__main__":
    test_alignment()
