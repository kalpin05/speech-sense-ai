import Levenshtein
import unicodedata
import logging
import json
from app.utils.feedback_translations import FEEDBACK_TRANSLATIONS

log = logging.getLogger(__name__)


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

    return json.dumps({
        "message": translations["excellent"] if accuracy > 90 else translations["good"] if accuracy > 75 else translations["close"].format(expected=expected) if accuracy > 50 else translations["poor"].format(expected=expected),
        "diff": diff,
        "incorrect_words": incorrect_words,
        "detailed_analysis": detailed_analysis
    })


def calculate_acoustic_features(file_path: str) -> dict:
    """Extract RMS energy and F0 pitch stats from audio file using librosa."""
    try:
        import librosa
        import numpy as np

        y, sr = librosa.load(file_path, sr=None)
        if len(y) < 100:
            return {"mean_energy": 0.0, "std_energy": 0.0, "mean_pitch": 0.0, "std_pitch": 0.0}

        # 1. Volume/Energy (RMS)
        rms = librosa.feature.rms(y=y)
        mean_energy = float(np.mean(rms))
        std_energy = float(np.std(rms))

        # 2. Fundamental Frequency (F0 Pitch tracking using Yin)
        mean_pitch = 0.0
        std_pitch = 0.0
        try:
            pitches = librosa.yin(y, fmin=60, fmax=400, sr=sr)
            voiced_pitches = pitches[~np.isnan(pitches)]
            voiced_pitches = voiced_pitches[voiced_pitches > 0]
            if len(voiced_pitches) > 0:
                mean_pitch = float(np.mean(voiced_pitches))
                std_pitch = float(np.std(voiced_pitches))
        except Exception as e:
            log.warning(f"Pitch detection failed: {e}. Falling back.")

        return {
            "mean_energy": mean_energy,
            "std_energy": std_energy,
            "mean_pitch": mean_pitch,
            "std_pitch": std_pitch
        }
    except Exception as e:
        log.error(f"Failed to calculate acoustic features: {e}")
        return {"mean_energy": 0.0, "std_energy": 0.0, "mean_pitch": 0.0, "std_pitch": 0.0}


# Language-specific speech filler words
FILLER_WORDS = {
    "english": ["um", "uh", "ah", "eh", "like", "well", "er", "you know"],
    "spanish": ["este", "bueno", "eh", "o sea", "pues", "sabes"],
    "hindi": ["मतलब", "अच्छा", "यानी", "जैसे कि"]
}

def detect_emotion_and_confidence(file_path: str, transcription: str, language_code: str = "en") -> dict:
    """Analyze acoustics and text transcript to estimate emotion, confidence, hesitation, and nervousness."""
    import os
    import json
    
    # Find active language
    lang = "english"
    if language_code == "es":
        lang = "spanish"
    elif language_code == "hi":
        lang = "hindi"

    # 1. Textual Analysis: Count fillers
    clean_trans = transcription.lower().strip()
    words = clean_trans.split()
    word_count = len(words)
    
    fillers = FILLER_WORDS.get(lang, FILLER_WORDS["english"])
    filler_count = 0
    for f in fillers:
        filler_count += clean_trans.count(f)

    # 2. Audio features
    acoustics = calculate_acoustic_features(file_path)
    mean_energy = acoustics["mean_energy"]
    std_energy = acoustics["std_energy"]
    mean_pitch = acoustics["mean_pitch"]
    std_pitch = acoustics["std_pitch"]

    # 3. Fetch pause and silence metrics from fluency
    fluency_data = calculate_real_fluency(file_path, transcription, language_code)
    pause_count = fluency_data.get("pause_count", 0)
    
    # Calculate silence ratio
    try:
        import librosa
        y, sr = librosa.load(file_path, sr=None)
        total_duration = len(y) / sr
        intervals = librosa.effects.split(y, top_db=25)
        speaking_duration = sum((end - start) / sr for start, end in intervals)
        silence_ratio = (total_duration - speaking_duration) / total_duration if total_duration > 0 else 0.0
    except Exception:
        silence_ratio = 0.2

    # 4. Compute Scores
    # A. Hesitation Score
    hesitation_pct = (pause_count / max(1.0, word_count)) * 200.0 + (filler_count * 15.0)
    hesitation_score = int(max(0, min(100, hesitation_pct)))

    # B. Nervousness Score
    speech_rate = fluency_data.get("speech_rate", 120.0)
    rate_dev = 0.0
    if speech_rate < 100:
        rate_dev = (100.0 - speech_rate) * 0.8
    elif speech_rate > 160:
        rate_dev = (speech_rate - 160.0) * 0.8
    
    pitch_jitter_penalty = 0.0
    if mean_pitch > 0:
        pitch_cv = std_pitch / mean_pitch
        if pitch_cv > 0.3:
            pitch_jitter_penalty = min(30.0, (pitch_cv - 0.3) * 100.0)
        elif pitch_cv < 0.05:
            pitch_jitter_penalty = 15.0

    nervousness_pct = rate_dev + (silence_ratio * 40.0) + pitch_jitter_penalty
    nervousness_score = int(max(0, min(100, nervousness_pct)))

    # C. Confidence Score
    conf = 100.0 - (hesitation_score * 0.4) - (nervousness_score * 0.4) - (silence_ratio * 20.0)
    if std_energy > 0 and mean_energy > 0:
        energy_cv = std_energy / mean_energy
        if energy_cv < 0.25:
            conf += 5
    confidence_score = int(max(0, min(100, conf)))

    # 5. Classify Dominant Emotion
    dominant_emotion = "neutral"

    # Check for OpenAI LLM if key is present
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            import urllib.request
            prompt = f"""
You are an advanced vocal analysis AI.
Analyze this speech sample data:
- Transcription: "{transcription}"
- Language: "{lang}"
- Acoustic pitch mean: {mean_pitch:.1f} Hz (std dev: {std_pitch:.1f})
- Acoustic volume/energy mean: {mean_energy:.4f} (std dev: {std_energy:.4f})
- Silence ratio: {silence_ratio:.2f}
- Speaking rate: {speech_rate:.1f} WPM
- Pause count: {pause_count}
- Filler words count: {filler_count}

Output a single JSON object containing:
- "confidence_score": integer 0-100
- "nervousness_score": integer 0-100
- "hesitation_score": integer 0-100
- "emotion": one of "happy", "anxious", "sad", "angry", "neutral"

Response format: ONLY valid JSON, no markdown codeblocks, no extra text.
"""
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }
            req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
            with urllib.request.urlopen(req, timeout=10) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                content = res_data["choices"][0]["message"]["content"].strip()
                if content.startswith("```"):
                    content = content.replace("```json", "").replace("```", "").strip()
                parsed = json.loads(content)
                return {
                    "confidence_score": int(parsed.get("confidence_score", confidence_score)),
                    "nervousness_score": int(parsed.get("nervousness_score", nervousness_score)),
                    "hesitation_score": int(parsed.get("hesitation_score", hesitation_score)),
                    "emotion": str(parsed.get("emotion", "neutral")).lower()
                }
        except Exception as e:
            log.error(f"Failed to analyze emotion/confidence via OpenAI: {e}. Falling back to rule-based.")

    # Rule-based fallback classifier
    positive_words = ["happy", "good", "great", "excellent", "nice", "love", "joy", "amazing", "bueno", "feliz", "alegre", "gracias", "सुंदर", "अच्छा", "धन्यवाद", "सफलता"]
    negative_words = ["sad", "bad", "angry", "hate", "sorry", "fear", "scared", "pain", "mal", "triste", "miedo", "enojado", "दुख", "खराब", "डर", "गुस्सा"]
    
    pos_count = sum(clean_trans.count(w) for w in positive_words)
    neg_count = sum(clean_trans.count(w) for w in negative_words)

    if mean_pitch > 0:
        pitch_cv = std_pitch / mean_pitch
    else:
        pitch_cv = 0.15

    if pos_count > neg_count:
        if pitch_cv > 0.22 or mean_energy > 0.04:
            dominant_emotion = "happy"
        else:
            dominant_emotion = "neutral"
    elif neg_count > pos_count:
        if nervousness_score > 50 or hesitation_score > 55:
            dominant_emotion = "anxious"
        elif pitch_cv < 0.08 and mean_energy < 0.015:
            dominant_emotion = "sad"
        else:
            dominant_emotion = "angry"
    else:
        if nervousness_score > 60 or (pitch_cv > 0.25 and hesitation_score > 40):
            dominant_emotion = "anxious"
        elif pitch_cv > 0.22 and mean_energy > 0.03:
            dominant_emotion = "happy"
        elif pitch_cv < 0.08 and mean_energy < 0.015:
            dominant_emotion = "sad"
        elif pitch_cv < 0.06 and mean_energy > 0.04:
            dominant_emotion = "angry"
        else:
            dominant_emotion = "neutral"

    return {
        "confidence_score": confidence_score,
        "nervousness_score": nervousness_score,
        "hesitation_score": hesitation_score,
        "emotion": dominant_emotion
    }


def analyze_language_weaknesses(weak_words: list[str], language: str) -> tuple[list[str], str]:
    """Identify language-specific weak sounds and generate customized practice drills."""
    lang_clean = language.lower().strip()
    
    # 1. Base case: no weak words
    if not weak_words:
        return [], "Excellent job! No weak words detected yet."
        
    weak_sounds = []
    custom_drill = ""
    words_str = ", ".join(weak_words[:5])
    
    if lang_clean == "spanish":
        sp_counts = {}
        for w in weak_words:
            w_lower = w.lower()
            if "rr" in w_lower:
                sp_counts["Rolled 'rr'"] = sp_counts.get("Rolled 'rr'", 0) + 1
            if w_lower.startswith("h"):
                sp_counts["Silent 'h'"] = sp_counts.get("Silent 'h'", 0) + 1
            if "ñ" in w_lower:
                sp_counts["Spanish 'ñ'"] = sp_counts.get("Spanish 'ñ'", 0) + 1
            if "ll" in w_lower:
                sp_counts["Double 'll'"] = sp_counts.get("Double 'll'", 0) + 1
            if w_lower.startswith("j") or w_lower.startswith("g"):
                sp_counts["Velar 'g/j'"] = sp_counts.get("Velar 'g/j'", 0) + 1
                
        sorted_sp = sorted(sp_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_sp if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Rolled 'rr'":
            custom_drill = "Practice rolling your tongue. Try saying: 'Erre con erre cigarro, erre con erre barril.'"
        elif top_weak == "Silent 'h'":
            custom_drill = "Remember, the letter 'h' is silent in Spanish. Try saying: 'Hola, hoy hago helado.'"
        elif top_weak == "Spanish 'ñ'":
            custom_drill = "Practice the 'ñ' sound. Try saying: 'Mañana el niño comerá piña.'"
        elif top_weak == "Double 'll'":
            custom_drill = "Practice the 'll' sound (y/ly). Try saying: 'La lluvia en Sevilla es una maravilla.'"
        elif top_weak == "Velar 'g/j'":
            custom_drill = "Practice the aspirated 'j' or 'g' sound. Try saying: 'El gato de José juega en la jaula.'"
        else:
            custom_drill = f"Practice saying these Spanish words: {words_str}"
            
    elif lang_clean in ["hindi", "marathi", "telugu"]:
        hi_counts = {}
        for w in weak_words:
            # 1. Retroflexes (ट, ठ, ड, ढ, ण, ట, డ, ఠ, ఢ, ణ, ट, ड)
            if any(c in w for c in ["ट", "ठ", "ड", "ढ", "ण", "ట", "డ", "ఠ", "ఢ", "ణ"]):
                hi_counts["Retroflex (ट/ड)"] = hi_counts.get("Retroflex (ट/ड)", 0) + 1
            
            # 2. Aspirates (ध, bh, gh, th, kh, ph)
            elif any(c in w for c in ["ध", "भ", "घ", "थ", "ख", "छ", "झ", "ठ", "ढ", "फ़", "ధ", "భ", "ఘ", "థ", "ఖ", "ఛ", "ఝ", "ఠ", "ఢ"]) or any(p in w.lower() for p in ["dh", "bh", "gh", "th", "kh", "ph"]):
                hi_counts["Aspirated (ध/भ/th)"] = hi_counts.get("Aspirated (ध/भ/th)", 0) + 1
                
            # 3. Nasalization (ँ, ं)
            elif any(c in w for c in ["ँ", "ं", "ఁ", "ం"]):
                hi_counts["Nasalized (ं/ँ)"] = hi_counts.get("Nasalized (ं/ँ)", 0) + 1
                
            # 4. Sibilants (श, ष, శ, ష)
            elif any(c in w for c in ["श", "ष", "శ", "ష"]) or w.lower().startswith("sh"):
                hi_counts["Sibilant (श/ष)"] = hi_counts.get("Sibilant (श/ष)", 0) + 1
                
        sorted_hi = sorted(hi_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_hi if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Retroflex (ट/ड)":
            custom_drill = "अपनी जीभ को ऊपर तालू से छुएं (Retroflex sound). बोलें: 'टमाटर ठंडा है, डालर लाओ।'"
        elif top_weak == "Aspirated (ध/भ/th)":
            custom_drill = "बोलते समय मुंह से हवा बाहर निकालें (Aspirated sound). बोलें: 'धर्म और धन बहुत भारी हैं।'"
        elif top_weak == "Nasalized (ं/ँ)":
            custom_drill = "नाक से आवाज निकालें (Nasalized sound). बोलें: 'चाँद सुंदर है, पतंग उड़ती है।'"
        elif top_weak == "Sibilant (श/ष)":
            custom_drill = "श और ष के अंतर को स्पष्ट करें। बोलें: 'शीला शाम को षड्यंत्र रचेगी।'"
        else:
            custom_drill = f"Practice these pronunciation targets: {words_str}"

    elif lang_clean == "tamil":
        ta_counts = {}
        for w in weak_words:
            if any(c in w for c in ["ழ", "ள", "ற", "ண", "ட"]):
                ta_counts["Retroflex (ழ/ள)"] = ta_counts.get("Retroflex (ழ/ள)", 0) + 1
            if any(c in w for c in ["க", "ச", "த", "ப"]):
                ta_counts["Plosives (க/ச)"] = ta_counts.get("Plosives (க/ச)", 0) + 1
                
        sorted_ta = sorted(ta_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_ta if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Retroflex (ழ/ள)":
            custom_drill = "Touch your tongue to the roof of your mouth for the Tamil retroflex. Practice: 'வாழைப்பழம் நல்ல பழம்.'"
        else:
            custom_drill = f"இவற்றை உச்சரிக்க பயிற்சி செய்யவும்: {words_str}"

    elif lang_clean == "german":
        de_counts = {}
        for w in weak_words:
            w_lower = w.lower()
            if any(c in w_lower for c in ["ä", "ö", "ü", "ß"]):
                de_counts["Umlaut (ä/ö/ü)"] = de_counts.get("Umlaut (ä/ö/ü)", 0) + 1
            if "ch" in w_lower or "sch" in w_lower:
                de_counts["Fricative (ch/sch)"] = de_counts.get("Fricative (ch/sch)", 0) + 1
                
        sorted_de = sorted(de_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_de if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Umlaut (ä/ö/ü)":
            custom_drill = "Practice the correct vowel shape for Umlauts. Try saying: 'Müllmänner müssen Öl wählen.'"
        elif top_weak == "Fricative (ch/sch)":
            custom_drill = "Practice soft fricative air release. Try saying: 'Fischers Fritz fischt frische Fische.'"
        else:
            custom_drill = f"Üben Sie die Aussprache dieser Wörter: {words_str}"

    elif lang_clean == "french":
        fr_counts = {}
        for w in weak_words:
            w_lower = w.lower()
            if any(p in w_lower for p in ["an", "en", "in", "on", "un"]):
                fr_counts["Nasal vowel (an/on)"] = fr_counts.get("Nasal vowel (an/on)", 0) + 1
            if "r" in w_lower:
                fr_counts["Uvular 'r'"] = fr_counts.get("Uvular 'r'", 0) + 1
                
        sorted_fr = sorted(fr_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_fr if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Nasal vowel (an/on)":
            custom_drill = "Let air pass through both nose and mouth. Try saying: 'Un bon vin blanc de l'an passé.'"
        elif top_weak == "Uvular 'r'":
            custom_drill = "Vibrate the back of your throat. Try saying: 'Le rat rouge court dans la rue.'"
        else:
            custom_drill = f"Entraînez-vous à prononcer ces mots: {words_str}"

    elif lang_clean == "japanese":
        ja_counts = {}
        for w in weak_words:
            if any(c in w for c in ["ら", "り", "る", "れ", "ろ"]) or "r" in w.lower() or "l" in w.lower():
                ja_counts["Liquid (r/l) sound"] = ja_counts.get("Liquid (r/l) sound", 0) + 1
            if "っ" in w or "ー" in w or any(p in w.lower() for p in ["kk", "ss", "tt", "pp"]):
                ja_counts["Double consonant (っ)"] = ja_counts.get("Double consonant (っ)", 0) + 1
                
        sorted_ja = sorted(ja_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_ja if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Liquid (r/l) sound":
            custom_drill = "Place your tongue between R and L. Try saying: '桜の木が綺麗に並んでいます。'"
        elif top_weak == "Double consonant (っ)":
            custom_drill = "Add a small pause before the double consonant. Try saying: '切符を買って学校へ行って。'"
        else:
            custom_drill = f"単語の発音を練習しましょう: {words_str}"

    elif lang_clean == "arabic":
        ar_counts = {}
        for w in weak_words:
            if any(c in w for c in ["ع", "ح", "خ", "ق", "ص", "ض", "ط", "ظ"]):
                ar_counts["Guttural sound"] = ar_counts.get("Guttural sound", 0) + 1
            if any(c in w for c in ["ا", "و", "ي"]):
                ar_counts["Long Vowel"] = ar_counts.get("Long Vowel", 0) + 1
                
        sorted_ar = sorted(ar_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_ar if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "Guttural sound":
            custom_drill = "Vibrate the back of your throat. Try saying: 'خالد يحب التفاح والقهوة العربية.'"
        else:
            custom_drill = f"تدرب على نطق هذه الكلمات: {words_str}"
            
    else:
        # Default/English patterns
        sound_patterns = ["th", "sh", "ch", "wh", "ph", "tr", "pl", "gr", "st", "sp", "h", "s", "f", "r", "l", "w", "v"]
        sound_counts = {}
        for w in weak_words:
            w_lower = w.lower()
            for pattern in sound_patterns:
                if w_lower.startswith(pattern) or (pattern in ["th", "sh", "ch"] and pattern in w_lower):
                    sound_counts[f"'{pattern}' sound"] = sound_counts.get(f"'{pattern}' sound", 0) + 1
                    break
        sorted_en = sorted(sound_counts.items(), key=lambda x: x[1], reverse=True)
        weak_sounds = [snd for snd, count in sorted_en if count >= 1]
        
        top_weak = weak_sounds[0] if weak_sounds else None
        if top_weak == "'th' sound":
            custom_drill = "Place your tongue between your teeth for 'th'. Practice: 'The three brothers thought of this.'"
        elif top_weak == "'r' sound":
            custom_drill = "Curl your tongue back without touching the roof. Practice: 'Red roses grow around the river.'"
        elif top_weak == "'w' sound" or top_weak == "'v' sound":
            custom_drill = "Clarify 'w' vs 'v'. Practice: 'We value very warm winter weather.'"
        elif top_weak:
            custom_drill = f"Focus on your {top_weak} weaknesses. Practice: 'She spoke simple sounds clearly.'"
        else:
            custom_drill = f"Practice saying these English words: {words_str}"
            
    return weak_sounds, custom_drill