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


def generate_feedback(expected: str, actual: str, accuracy: float, language_code: str = "en") -> str:
    translations = FEEDBACK_TRANSLATIONS.get(language_code, FEEDBACK_TRANSLATIONS["en"])
    
    if accuracy > 90:
        return translations["excellent"]
    elif accuracy > 75:
        return translations["good"]
    elif accuracy > 50:
        return translations["close"].format(expected=expected)
    else:
        return translations["poor"].format(expected=expected)