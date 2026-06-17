import Levenshtein
import unicodedata
from app.utils.feedback_translations import FEEDBACK_TRANSLATIONS


def normalize_text(text: str) -> str:
    text = text.lower()
    # Remove punctuation using unicodedata to safely preserve non-Latin marks/vowels
    text = "".join(ch for ch in text if not unicodedata.category(ch).startswith('P'))
    text = text.strip()
    return text


def calculate_accuracy(expected: str, actual: str) -> float:
    expected = normalize_text(expected)
    actual = normalize_text(actual)

    distance = Levenshtein.distance(expected, actual)
    max_len = max(len(expected), len(actual))

    if max_len == 0:
        return 100.0

    accuracy = (1 - distance / max_len) * 100
    return round(accuracy, 2)


def calculate_fluency(transcription: str, language_code: str = "en") -> str:
    # Japanese spacing issue (no spaces). We use a character heuristic ~2.5 chars per word equivalent
    if language_code == "ja":
        equivalent_word_count = len(transcription.strip()) / 2.5
        word_count = equivalent_word_count
    else:
        words = transcription.split()
        word_count = len(words)

    if word_count == 0:
        return "poor"
    elif word_count < 3:
        return "poor"
    elif word_count < 7:
        return "medium"
    else:
        return "good"


import difflib

def generate_feedback(expected: str, actual: str, accuracy: float, language_code: str = "en") -> str:
    translations = FEEDBACK_TRANSLATIONS.get(language_code, FEEDBACK_TRANSLATIONS["en"])
    
    # Generate word-level diff
    expected_words = normalize_text(expected).split()
    actual_words = normalize_text(actual).split()
    
    diff = []
    matcher = difflib.SequenceMatcher(None, expected_words, actual_words)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            for w in expected_words[i1:i2]:
                diff.append({"word": w, "status": "correct"})
        elif tag == 'replace':
            for w in expected_words[i1:i2]:
                diff.append({"word": w, "status": "missed"})
            for w in actual_words[j1:j2]:
                diff.append({"word": w, "status": "extra"})
        elif tag == 'delete':
            for w in expected_words[i1:i2]:
                diff.append({"word": w, "status": "missed"})
        elif tag == 'insert':
            for w in actual_words[j1:j2]:
                diff.append({"word": w, "status": "extra"})

    # Instead of just returning a string, we return a JSON stringified dict or rely on main.py to pass dicts.
    # To avoid breaking existing database schemas (which expect a string), we'll format the string with HTML/JSON
    import json
    return json.dumps({
        "message": translations["excellent"] if accuracy > 90 else translations["good"] if accuracy > 75 else translations["close"].format(expected=expected) if accuracy > 50 else translations["poor"].format(expected=expected),
        "diff": diff
    })