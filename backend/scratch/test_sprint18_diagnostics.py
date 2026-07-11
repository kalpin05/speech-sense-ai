import sys
import os

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.analysis_service import analyze_language_weaknesses

def test_sprint18_diagnostics():
    print("--- Running Sprint 18 Language-Specific Diagnostics Tests ---")
    
    # 1. Test Spanish Diagnostics
    print("1. Testing Spanish rolled rr...")
    weak_es_rr, drill_es_rr = analyze_language_weaknesses(["perro", "correr"], "spanish")
    assert "Rolled 'rr'" in weak_es_rr, f"Expected Rolled 'rr', got {weak_es_rr}"
    assert "erre con erre" in drill_es_rr.lower(), f"Unexpected drill: {drill_es_rr}"
    
    print("2. Testing Spanish silent h...")
    weak_es_h, drill_es_h = analyze_language_weaknesses(["hola", "hablar"], "spanish")
    assert "Silent 'h'" in weak_es_h, f"Expected Silent 'h', got {weak_es_h}"
    assert "silent" in drill_es_h.lower(), f"Unexpected drill: {drill_es_h}"
    
    print("3. Testing Spanish n-tilde...")
    weak_es_n, drill_es_n = analyze_language_weaknesses(["niño", "piña"], "spanish")
    assert "Spanish 'ñ'" in weak_es_n, f"Expected Spanish 'ñ', got {weak_es_n}"
    assert "mañana" in drill_es_n.lower(), f"Unexpected drill: {drill_es_n}"

    # 2. Test Hindi Diagnostics
    print("4. Testing Hindi retroflex...")
    weak_hi_ret, drill_hi_ret = analyze_language_weaknesses(["टमाटर", "ठंडा"], "hindi")
    assert "Retroflex (ट/ड)" in weak_hi_ret, f"Expected Retroflex (ट/ड), got {weak_hi_ret}"
    
    print("5. Testing Hindi aspirates...")
    weak_hi_asp, drill_hi_asp = analyze_language_weaknesses(["धर्म", "dhan"], "hindi")
    assert "Aspirated (ध/भ/th)" in weak_hi_asp, f"Expected Aspirated, got {weak_hi_asp}"
    
    print("6. Testing Hindi nasalized...")
    weak_hi_nas, drill_hi_nas = analyze_language_weaknesses(["चाँद", "पतंग"], "hindi")
    assert "Nasalized (ं/ँ)" in weak_hi_nas, f"Expected Nasalized, got {weak_hi_nas}"

    # 3. Test English Diagnostics
    print("7. Testing English th...")
    weak_en_th, drill_en_th = analyze_language_weaknesses(["think", "brother"], "english")
    assert "'th' sound" in weak_en_th, f"Expected 'th' sound, got {weak_en_th}"
    assert "three brothers" in drill_en_th.lower(), f"Unexpected drill: {drill_en_th}"
    
    print("8. Testing English r...")
    weak_en_r, drill_en_r = analyze_language_weaknesses(["run", "river"], "english")
    assert "'r' sound" in weak_en_r, f"Expected 'r' sound, got {weak_en_r}"
    assert "red roses" in drill_en_r.lower(), f"Unexpected drill: {drill_en_r}"

    print("\nAll language-specific pronunciation diagnostics checks passed successfully!")

if __name__ == "__main__":
    test_sprint18_diagnostics()
