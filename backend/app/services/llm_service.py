import os
import json
import urllib.request
import logging

log = logging.getLogger(__name__)

# Rich templates for rule-based local generator (multilingual fallback)
TEMPLATES = {
    "english": {
        "weak_sounds": {
            "th": [
                "Three thin thieves thought of thirty thousand thanks.",
                "This is the path they took through the thick forest.",
                "Both brothers bathe together in the northern river."
            ],
            "sh": [
                "She sells sea shells by the sea shore.",
                "The shiny silver ship sank in the shallow ocean.",
                "Wish you a fresh show of shoes and shirts."
            ],
            "ch": [
                "Children cheer for chicken and chips.",
                "Charlie chose to chew cherry chocolate.",
                "Watch the coach catch the cheap match."
            ],
            "s": [
                "Sally sings sweet songs on Sunday.",
                "Seven slippery snakes slid slowly southward.",
                "Six sick sheep sat on the soft grass."
            ],
            "r": [
                "Red roses rise rapidly in the rain.",
                "Robert ran round the rugged rock.",
                "The green frog leaped over the yellow river."
            ],
            "l": [
                "Light yellow lemons look lovely.",
                "Little Lily loves listing large letters.",
                "Play the clean flute slowly near the lake."
            ],
            "f": [
                "Fred fed five friends fresh fruit.",
                "Five brave victims visited the fine valley.",
                "Fiona found forty feathers on the farm."
            ],
            "v": [
                "Vera values very vivid velvet shirts.",
                "Valerie drove the van to the village valley.",
                "Every heavy wave covers the river cove."
            ]
        },
        "sentence": {
            "beginner": [
                "The cat sat on the mat.",
                "I see a blue bird in the tree.",
                "Water is good for your health."
            ],
            "intermediate": [
                "A balanced diet and regular exercise keep you healthy.",
                "We decided to take a walk along the river bank.",
                "Learning new skills can be challenging but rewarding."
            ],
            "advanced": [
                "Artificial intelligence is transforming modern industries rapidly.",
                "Success requires persistence, dedication, and clear focus.",
                "Environmental sustainability is a critical global challenge."
            ]
        },
        "passage": {
            "beginner": [
                "Yesterday was a sunny day. I went to the park with my friends. We played soccer and ate ice cream. It was a lot of fun."
            ],
            "intermediate": [
                "Reading books is a wonderful habit. It not only expands your vocabulary but also opens your mind to new perspectives. Many people prefer reading before bed to relax after a busy day."
            ],
            "advanced": [
                "The rapid evolution of technology has revolutionized human communication. While digital platforms connect people globally, they also present complex challenges regarding privacy and screen time management. Balancing virtual connectivity with real-world interactions remains vital."
            ]
        },
        "drill": {
            "beginner": [
                "Peter Piper picked a peck of pickled peppers.",
                "I scream, you scream, we all scream for ice cream.",
                "Red leather, yellow leather."
            ],
            "intermediate": [
                "Betty Botter bought some butter, but she said the butter's bitter.",
                "How much wood would a woodchuck chuck if a woodchuck could chuck wood?",
                "A tutor who tooted the flute tried to tutor two tooters to toot."
            ],
            "advanced": [
                "If you must cross a coarse cross cow across a crowded cow crossing, cross the cross cow carefully.",
                "She saw Sharif's shoes on the sofa, but Sharif saw she saw his shoes.",
                "Top chopstick shops stock top chopsticks."
            ]
        },
        "repetition": {
            "beginner": ["Happy, Apple, Water, Table, Morning"],
            "intermediate": ["Beautiful, Chocolate, Vocabulary, Conversation, Wonderful"],
            "advanced": ["Unprecedented, Characteristically, Phenomenon, Chronological, Sustainability"]
        }
    },
    "spanish": {
        "weak_sounds": {
            "r": [
                "Tres tristes tigres tragan trigo en un trigal.",
                "El perro de San Roque no tiene rabo porque Ramón Ramírez se lo ha cortado.",
                "Rápido corren los carros cargados de azúcar del ferrocarril."
            ],
            "rr": [
                "El perro corre rápido por el cerro.",
                "El carro tiene cuatro ruedas redondas.",
                "Ramón y Rosa corren por la carretera."
            ],
            "j": [
                "El joven jinete juega con la jirafa en el jardín.",
                "Los ojos rojos del conejo bajo la esponja.",
                "José junta jarras de jugo junto al cajón."
            ]
        },
        "sentence": {
            "beginner": [
                "El sol brilla en el cielo.",
                "Me gusta comer manzanas rojas.",
                "Hola, ¿cómo te llamas tú?"
            ],
            "intermediate": [
                "El aprendizaje de idiomas requiere mucha paciencia y práctica.",
                "Ayer fuimos de paseo por el parque de la ciudad.",
                "Me gustaría reservar una mesa para cenar esta noche."
            ],
            "advanced": [
                "La tecnología moderna ha cambiado drásticamente la vida cotidiana.",
                "Es fundamental proteger el medio ambiente para las futuras generaciones.",
                "El desarrollo económico sostenible presenta desafíos complejos a nivel global."
            ]
        },
        "passage": {
            "beginner": [
                "Ayer fue un día soleado. Fui al parque con mis amigos. Jugamos al fútbol y comimos helado de fresa. Fue muy divertido."
            ],
            "intermediate": [
                "Leer libros es un hábito maravilloso. No solo expande tu vocabulario sino que también abre tu mente a nuevas perspectivas de vida. Muchas personas leen antes de dormir para relajarse."
            ],
            "advanced": [
                "La evolución de la inteligencia artificial está transformando rápidamente diversas industrias en todo el mundo. Si bien esto genera oportunidades sin precedentes, también suscita debates éticos profundos sobre la automatización del trabajo y la privacidad."
            ]
        },
        "drill": {
            "beginner": [
                "Pablito clavó un clavito en la calva de un calvito.",
                "Como poco coco como, poco coco compro.",
                "Tres tristes tigres tragan trigo."
            ],
            "intermediate": [
                "María Chuchena techaba su choza, y un techador que por allí pasaba le dijo: María Chuchena, ¿techas tu choza o techas la ajena?",
                "El cielo está encapotado, ¿quién lo desencapotará?",
                "Cuando cuentes cuentos, cuenta cuántos cuentos cuentas."
            ],
            "advanced": [
                "El arzobispo de Constantinopla se quiere desarzobispoconstantinopolizar, el desarzobispoconstantinopolizador que lo desarzobispoconstantinopolice, buen desarzobispoconstantinopolizador será."
            ]
        },
        "repetition": {
            "beginner": ["Hola, Casa, Perro, Gato, Mesa"],
            "intermediate": ["Biblioteca, Maravilloso, Computadora, Estudiante, Película"],
            "advanced": ["Desafortunadamente, Constitucionalidad, Electroencefalograma, Característica"]
        }
    },
    "hindi": {
        "weak_sounds": {
            "sh": [
                "शीला ने साफ शीशे को शान से सजाया।",
                "शाम को शशिकांत ने शांत होकर शंख बजाया।"
            ],
            "r": [
                "लड़का लकड़ी लेकर सड़क पर दौड़ रहा था।",
                "रामू रात में रोते-रोते रास्ता भूल गया।"
            ]
        },
        "sentence": {
            "beginner": [
                "यह एक सुंदर बगीचा है।",
                "मुझे फल खाना पसंद है।",
                "आप कैसे हैं?"
            ],
            "intermediate": [
                "कल सुबह हम सब मिलकर पिकनिक पर जा रहे हैं।",
                "किताबें पढ़ना ज्ञान बढ़ाने का सबसे अच्छा साधन है।",
                "नियमित व्यायाम स्वास्थ्य के लिए बहुत लाभदायक है।"
            ],
            "advanced": [
                "वैज्ञानिक प्रगति ने मानव जीवन को अत्यंत सुगम बना दिया है।",
                "पर्यावरण संरक्षण प्रत्येक नागरिक का नैतिक कर्तव्य है।",
                "सफलता प्राप्त करने के लिए निरंतर परिश्रम और दृढ़ संकल्प आवश्यक है।"
            ]
        },
        "passage": {
            "beginner": [
                "आज मौसम बहुत अच्छा है। आसमान में बादल छाए हुए हैं। हम सब आज बाहर घूमने जाएंगे और मजे करेंगे।"
            ],
            "intermediate": [
                "स्वस्थ शरीर में ही स्वस्थ मस्तिष्क का निवास होता है। हमें अपने स्वास्थ्य के प्रति सदैव सजग रहना चाहिए। संतुलित आहार और ध्यान इसके प्रमुख साधन हैं।"
            ],
            "advanced": [
                "सूचना प्रौद्योगिकी के इस युग में इंटरनेट मानव जीवन का अभिन्न अंग बन गया है। इसने भौगोलिक दूरियों को समाप्त कर पूरे विश्व को एक सूत्र में पिरो दिया है, परंतु इसके अत्यधिक उपयोग के दुष्परिणामों से बचना आवश्यक है।"
            ]
        },
        "drill": {
            "beginner": [
                "चंदू के चाचा ने चंदू की चाची को चटनी चटाई।",
                "खड़क सिंह के खड़कने से खड़कती हैं खिड़कियां।",
                "पके पेड़ पर पका पपीता।"
            ],
            "intermediate": [
                "कच्चा पापड़ पक्का पापड़।",
                "डबल डमरू डिगा डिगा, डिगा डिगा डमरू डबल।",
                "चिट्ठी लेकर डाकिया दौड़ता-दौड़ता डाकिया घर गया।"
            ],
            "advanced": [
                "समझ समझ के समझ को समझो, समझ समझना भी एक समझ है, समझ समझ के जो ना समझे, मेरी समझ में वो नासमझ है।"
            ]
        },
        "repetition": {
            "beginner": ["नमस्ते, पानी, खाना, फल, घर"],
            "intermediate": ["धन्यवाद, सुंदर, विद्यालय, पुस्तक, मित्र"],
            "advanced": ["प्रतियोगिता, स्वावलंबन, संवेदनशीलता, औद्योगिकीकरण"]
        }
    }
}

def generate_fallback_exercises(language: str, difficulty: str, exercise_type: str, weak_sounds: list[str]) -> list[str]:
    """Fallback generator using static phonetic templates."""
    lang = language.lower()
    diff = difficulty.lower()
    ex_type = exercise_type.lower()
    
    # Defaults
    if lang not in TEMPLATES:
        lang = "english"
    if diff not in ["beginner", "intermediate", "advanced"]:
        diff = "beginner"
    if ex_type not in ["sentence", "passage", "drill", "repetition"]:
        ex_type = "sentence"
        
    db = TEMPLATES[lang]
    
    # 1. If weak sounds are requested and exist for this language
    if weak_sounds and "weak_sounds" in db:
        weak_exercises = []
        for sound in weak_sounds:
            sound_clean = sound.lower().strip()
            if sound_clean in db["weak_sounds"]:
                weak_exercises.extend(db["weak_sounds"][sound_clean])
        if len(weak_exercises) >= 3:
            return list(set(weak_exercises))[:3]
        elif len(weak_exercises) > 0:
            # Fall back to padding with normal exercises
            padding = db[ex_type][diff]
            combined = list(set(weak_exercises + padding))
            return combined[:3]
            
    # 2. Return standard template exercises
    res = db[ex_type].get(diff, db["sentence"]["beginner"])
    
    # Handle single string array items (like passages) or duplicates
    if len(res) < 3:
        # Pad with other difficulties or default sentences
        res = list(res)
        while len(res) < 3:
            res.append(f"Practice reading exercise drill number {len(res) + 1}.")
            
    return res[:3]

def generate_custom_exercises(language: str, difficulty: str, exercise_type: str, weak_sounds: list[str]) -> list[str]:
    """Generate custom exercises using OpenAI Chat Completion with urllib fallback."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        log.info("OPENAI_API_KEY not found in environment, falling back to local generator")
        return generate_fallback_exercises(language, difficulty, exercise_type, weak_sounds)

    weak_sounds_str = ", ".join(weak_sounds) if weak_sounds else "none"
    prompt = f"""
You are an expert Speech-Language Pathologist (SLP).
Generate exactly 3 customized practice exercises in language: '{language}' for a '{difficulty}' level student.
The type of exercises must be: '{exercise_type}'.

Guidelines:
- If exercise_type is 'sentence', generate short practice sentences.
- If exercise_type is 'passage', generate a short paragraph/reading passage.
- If exercise_type is 'drill', generate tongue twisters or phoneme contrast drills.
- If exercise_type is 'repetition', generate a list of target words.
- Focus on these weak sounds/letters if provided: '{weak_sounds_str}'. Emphasize them heavily in the output.

Response format:
Return ONLY a valid JSON list of 3 strings. Do not include markdown code block formatting (like ```json) or any conversational text.
Example:
["first exercise", "second exercise", "third exercise"]
"""

    try:
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            content = res_data["choices"][0]["message"]["content"].strip()
            
            # Clean formatting wrapper if present
            if content.startswith("```"):
                content = content.replace("```json", "").replace("```", "").strip()
                
            exercises = json.loads(content)
            if isinstance(exercises, list) and len(exercises) > 0:
                return [str(e).strip() for e in exercises]
                
    except Exception as e:
        log.error(f"Failed to generate exercises via OpenAI: {e}. Falling back to local generator.")
        
    return generate_fallback_exercises(language, difficulty, exercise_type, weak_sounds)
