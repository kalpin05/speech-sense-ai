import sys
import os

# Add the backend dir to sys.path so we can import app modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")

from app.services.analysis_service import normalize_text, calculate_fluency, generate_feedback

def test_normalization():
    print("--- Normalization ---")
    texts = [
        "Hello, World!",                    # English
        "नमस्ते, आप कैसे हैं?",               # Hindi
        "こんにちは、元気ですか？",            # Japanese
        "مرحباً، كيف حالك؟"                  # Arabic
    ]
    for t in texts:
        print(f"Original: {t} -> Normalized: {normalize_text(t)}")

def test_fluency():
    print("\n--- Fluency ---")
    en_text = "This is a good sentence for testing."
    ja_text = "これはテストのための良い文です。"
    print(f"EN (words={len(en_text.split())}): {calculate_fluency(en_text, 'en')}")
    print(f"JA (chars={len(ja_text)}): {calculate_fluency(ja_text, 'ja')}")

def test_feedback():
    print("\n--- Feedback ---")
    print(generate_feedback("hello", "hello", 95.0, "en"))
    print(generate_feedback("hello", "hello", 80.0, "hi"))
    print(generate_feedback("hello", "hello", 60.0, "ja"))
    print(generate_feedback("hello", "hello", 40.0, "ar"))

if __name__ == "__main__":
    test_normalization()
    test_fluency()
    test_feedback()
