import sys
import os

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.exercises_db import EXERCISES_DB
from app.utils.language_map import LANGUAGE_MAP
from app.services.analysis_service import analyze_language_weaknesses

def test_10_languages():
    print("--- Running 10 Languages Verification Tests ---")
    
    # 1. Check LANGUAGE_MAP
    expected_languages = [
        "english", "hindi", "marathi", "tamil", "telugu",
        "german", "french", "spanish", "japanese", "arabic"
    ]
    for lang in expected_languages:
        assert lang in LANGUAGE_MAP, f"Missing language in map: {lang}"
        assert lang in EXERCISES_DB, f"Missing exercises for: {lang}"
        
        # Verify basic structure of exercises
        levels = EXERCISES_DB[lang]
        for lvl in ["beginner", "intermediate", "advanced"]:
            assert lvl in levels, f"Missing level {lvl} for {lang}"
            assert len(levels[lvl]) > 0, f"No sentences in {lang} -> {lvl}"
            
    print("1. All 10 languages exist in map and exercises database.")

    # 2. Verify Phonetic Diagnostics for new languages
    print("2. Testing phonetic weaknesses for new languages...")
    
    # German Umlaut
    weak_de, drill_de = analyze_language_weaknesses(["müllmänner", "üben"], "german")
    assert "Umlaut (ä/ö/ü)" in weak_de
    assert "Müllmänner" in drill_de
    
    # French Nasal
    weak_fr, drill_fr = analyze_language_weaknesses(["blanc", "vin"], "french")
    assert "Nasal vowel (an/on)" in weak_fr
    assert "blanc" in drill_fr
    
    # Japanese Liquid
    weak_ja, drill_ja = analyze_language_weaknesses(["さくら", "kirei"], "japanese")
    assert "Liquid (r/l) sound" in weak_ja
    assert "桜" in drill_ja

    # Arabic Guttural
    weak_ar, drill_ar = analyze_language_weaknesses(["خالد", "قهوة"], "arabic")
    assert "Guttural sound" in weak_ar
    assert "خالد" in drill_ar

    # Tamil Retroflex
    weak_ta, drill_ta = analyze_language_weaknesses(["பழம்", "வாழை"], "tamil")
    assert "Retroflex (ழ/ள)" in weak_ta
    assert "வாழைப்பழம்" in drill_ta

    # Marathi/Telugu Retroflex
    weak_mr, drill_mr = analyze_language_weaknesses(["टमाटर", "ठंडा"], "marathi")
    assert "Retroflex (ट/ड)" in weak_mr

    print("\nAll 10-language diagnostics and seeder tests passed successfully!")

if __name__ == "__main__":
    test_10_languages()
