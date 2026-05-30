import whisper

model = whisper.load_model("turbo")


def transcribe_audio(file_path: str, language_code: str):
    result = model.transcribe(
        file_path,
        language=language_code,   # 🔥 FORCE LANGUAGE
        task="transcribe"
    )

    return result["text"].strip()