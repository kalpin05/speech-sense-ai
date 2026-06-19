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

def clean_word(word: str) -> str:
    word = word.lower().strip()
    word = "".join(ch for ch in word if not unicodedata.category(ch).startswith('P'))
    return word


def align_words_needleman_wunsch(expected_words: list[str], transcribed_words: list[dict]) -> list[tuple[int | None, int | None]]:
    import Levenshtein
    N = len(expected_words)
    M = len(transcribed_words)
    
    # Initialize DP table
    dp = [[0.0] * (M + 1) for _ in range(N + 1)]
    
    # Base cases
    for i in range(1, N + 1):
        dp[i][0] = dp[i-1][0] + 1.0
    for j in range(1, M + 1):
        dp[0][j] = dp[0][j-1] + 1.0
        
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            w_exp = clean_word(expected_words[i-1])
            w_trans = clean_word(transcribed_words[j-1].get("word", ""))
            
            # Match / Mismatch cost
            if w_exp == w_trans:
                match_cost = 0.0
            else:
                dist = Levenshtein.distance(w_exp, w_trans)
                max_len = max(len(w_exp), len(w_trans))
                if max_len > 0 and dist <= 2 and (dist / max_len) <= 0.4:
                    match_cost = (dist / max_len) * 0.5
                else:
                    match_cost = 1.0
                    
            dp[i][j] = min(
                dp[i-1][j-1] + match_cost, # Match / Mismatch
                dp[i-1][j] + 1.0,           # Deletion (Expected word omitted)
                dp[i][j-1] + 1.0            # Insertion (Extra word transcribed)
            )
            
    # Backtrack to find alignment path
    i, j = N, M
    alignment = []
    
    while i > 0 or j > 0:
        if i > 0 and j > 0:
            w_exp = clean_word(expected_words[i-1])
            w_trans = clean_word(transcribed_words[j-1].get("word", ""))
            if w_exp == w_trans:
                match_cost = 0.0
            else:
                dist = Levenshtein.distance(w_exp, w_trans)
                max_len = max(len(w_exp), len(w_trans))
                if max_len > 0 and dist <= 2 and (dist / max_len) <= 0.4:
                    match_cost = (dist / max_len) * 0.5
                else:
                    match_cost = 1.0
            
            if abs(dp[i][j] - (dp[i-1][j-1] + match_cost)) < 1e-5:
                alignment.append((i-1, j-1))
                i -= 1
                j -= 1
                continue
                
        if i > 0 and (j == 0 or abs(dp[i][j] - (dp[i-1][j] + 1.0)) < 1e-5):
            alignment.append((i-1, None))
            i -= 1
        else:
            alignment.append((None, j-1))
            j -= 1
            
    alignment.reverse()
    return alignment


def analyze_pronunciation(expected_text: str, whisper_result: dict, language_code: str = "en") -> dict:
    expected_words = expected_text.split()
    
    # Extract word objects from whisper_result
    transcribed_words = []
    if whisper_result and "segments" in whisper_result:
        for segment in whisper_result.get("segments", []):
            for w_obj in segment.get("words", []):
                transcribed_words.append(w_obj)
                
    # Fallback to simple matching if no word-level segment objects exist
    if not transcribed_words:
        detailed_analysis = []
        incorrect_words = []
        actual_text = whisper_result.get("text", "") if isinstance(whisper_result, dict) else ""
        actual_words = actual_text.split()
        
        for exp_word in expected_words:
            w_exp_clean = clean_word(exp_word)
            matched = False
            for act_word in actual_words:
                if clean_word(act_word) == w_exp_clean:
                    matched = True
                    break
            
            if matched:
                detailed_analysis.append({
                    "word": exp_word,
                    "status": "correct",
                    "error_type": "none",
                    "confidence": 1.0,
                    "start": 0.0,
                    "end": 0.0
                })
            else:
                incorrect_words.append(exp_word)
                detailed_analysis.append({
                    "word": exp_word,
                    "status": "incorrect",
                    "error_type": "mispronounced",
                    "confidence": 0.0,
                    "start": 0.0,
                    "end": 0.0
                })
        return {
            "incorrect_words": incorrect_words,
            "detailed_analysis": detailed_analysis
        }
        
    # Align sequences using Needleman-Wunsch
    alignment = align_words_needleman_wunsch(expected_words, transcribed_words)
    
    detailed_analysis = []
    incorrect_words = []
    
    # Map expected word index -> transcribed word index
    expected_map = {}
    for exp_idx, trans_idx in alignment:
        if exp_idx is not None:
            expected_map[exp_idx] = trans_idx
            
    for i, exp_word in enumerate(expected_words):
        trans_idx = expected_map.get(i)
        
        if trans_idx is not None:
            w_obj = transcribed_words[trans_idx]
            w_trans_clean = clean_word(w_obj.get("word", ""))
            w_exp_clean = clean_word(exp_word)
            prob = w_obj.get("probability", 1.0)
            start = w_obj.get("start", 0.0)
            end = w_obj.get("end", 0.0)
            
            if w_exp_clean != w_trans_clean:
                status = "incorrect"
                error_type = "mispronounced"
                incorrect_words.append(exp_word)
            elif prob < 0.70:
                status = "incorrect"
                error_type = "mispronounced"
                incorrect_words.append(exp_word)
            else:
                status = "correct"
                error_type = "none"
                
            detailed_analysis.append({
                "word": exp_word,
                "status": status,
                "error_type": error_type,
                "confidence": round(prob, 2),
                "start": round(start, 2),
                "end": round(end, 2)
            })
        else:
            incorrect_words.append(exp_word)
            detailed_analysis.append({
                "word": exp_word,
                "status": "incorrect",
                "error_type": "omitted",
                "confidence": 0.0,
                "start": 0.0,
                "end": 0.0
            })
            
    return {
        "incorrect_words": incorrect_words,
        "detailed_analysis": detailed_analysis
    }


def generate_feedback(expected: str, actual: str, accuracy: float, language_code: str = "en", whisper_result: dict = None) -> str:
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

    # Detailed pronunciation analysis
    incorrect_words = []
    detailed_analysis = []
    if whisper_result is not None:
        pron_analysis = analyze_pronunciation(expected, whisper_result, language_code)
        incorrect_words = pron_analysis["incorrect_words"]
        detailed_analysis = pron_analysis["detailed_analysis"]
    else:
        pron_analysis = analyze_pronunciation(expected, {"text": actual}, language_code)
        incorrect_words = pron_analysis["incorrect_words"]
        detailed_analysis = pron_analysis["detailed_analysis"]

    import json
    return json.dumps({
        "message": translations["excellent"] if accuracy > 90 else translations["good"] if accuracy > 75 else translations["close"].format(expected=expected) if accuracy > 50 else translations["poor"].format(expected=expected),
        "diff": diff,
        "incorrect_words": incorrect_words,
        "detailed_analysis": detailed_analysis
    })