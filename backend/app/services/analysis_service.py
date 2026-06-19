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


def calculate_real_fluency(file_path: str, transcription: str, language_code: str = "en") -> dict:
    try:
        import librosa
        import numpy as np

        # Load audio file (sr=None preserves native sampling rate)
        y, sr = librosa.load(file_path, sr=None)
        total_duration = len(y) / sr

        # Avoid division by zero for extremely short files
        if total_duration < 0.1:
            return {
                "fluency_score": 0,
                "speech_rate": 0,
                "pause_count": 0,
                "category": "poor"
            }

        # 1. Non-silent intervals detection
        # top_db=25 means silence is considered anything 25dB below the reference peak
        intervals = librosa.effects.split(y, top_db=25)
        
        # Calculate speaking duration (sum of non-silent intervals)
        speaking_duration = 0.0
        for start, end in intervals:
            speaking_duration += (end - start) / sr
            
        silence_duration = total_duration - speaking_duration

        # 2. Pause detection
        # We determine pauses as silent intervals between speaking segments that are >= 0.4 seconds (400ms)
        pause_count = 0
        if len(intervals) > 1:
            for i in range(len(intervals) - 1):
                # The end of the current segment to the start of the next segment is a gap
                gap_start = intervals[i][1]
                gap_end = intervals[i+1][0]
                gap_duration = (gap_end - gap_start) / sr
                if gap_duration >= 0.4:
                    pause_count += 1

        # 3. Speech Rate (WPM)
        # Handle word count heuristics for non-space languages (like Japanese)
        if language_code == "ja":
            word_count = len(transcription.strip()) / 2.5
        else:
            word_count = len(transcription.split())

        # Speaking rate = words per minute of speaking time (excluding long silence)
        if total_duration > 0:
            speech_rate = (word_count / total_duration) * 60.0
        else:
            speech_rate = 0.0

        # 4. Fluency Score calculation (starts at 100, drops on penalties)
        score = 100.0

        # A. Speed penalty
        # Optimal speaking rate is 110 - 150 WPM.
        # Penalty for too slow (WPM < 100) or too fast (WPM > 160)
        speed_penalty = 0.0
        if speech_rate < 100:
            speed_penalty = min(35.0, (100.0 - speech_rate) * 0.4)
        elif speech_rate > 160:
            speed_penalty = min(30.0, (speech_rate - 160.0) * 0.3)
        score -= speed_penalty

        # B. Pause penalty
        # We expect a normal number of pauses based on the size of the sentence (e.g., 1 pause per 6 words, min 1)
        expected_pauses = max(1.0, word_count / 6.0)
        pause_penalty = 0.0
        if pause_count > expected_pauses:
            pause_penalty = min(35.0, (pause_count - expected_pauses) * 6.0)
        score -= pause_penalty

        # C. Silence ratio penalty
        # If silence takes up more than 35% of the total duration, apply a penalty
        silence_ratio = silence_duration / total_duration if total_duration > 0 else 0
        silence_penalty = 0.0
        if silence_ratio > 0.35:
            silence_penalty = min(30.0, (silence_ratio - 0.35) * 100.0)
        score -= silence_penalty

        # Clamp score between 0 and 100
        fluency_score = int(max(0.0, min(100.0, score)))

        # Categorize
        if fluency_score >= 80:
            category = "good"
        elif fluency_score >= 50:
            category = "medium"
        else:
            category = "poor"

        return {
            "fluency_score": fluency_score,
            "speech_rate": int(round(speech_rate)),
            "pause_count": pause_count,
            "category": category
        }

    except Exception as e:
        # Fallback to simple heuristic if librosa fails or imports fail
        word_count = len(transcription.strip()) / 2.5 if language_code == "ja" else len(transcription.split())
        
        if word_count == 0:
            category = "poor"
            fluency_score = 0
            speech_rate = 0
        elif word_count < 3:
            category = "poor"
            fluency_score = 30
            speech_rate = 60
        elif word_count < 7:
            category = "medium"
            fluency_score = 65
            speech_rate = 110
        else:
            category = "good"
            fluency_score = 85
            speech_rate = 130

        return {
            "fluency_score": fluency_score,
            "speech_rate": speech_rate,
            "pause_count": 0,
            "category": category
        }


def calculate_fluency(transcription: str, language_code: str = "en") -> str:
    # Retained for basic backward compatibility, calls the simple heuristic
    word_count = len(transcription.strip()) / 2.5 if language_code == "ja" else len(transcription.split())
    if word_count == 0 or word_count < 3:
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