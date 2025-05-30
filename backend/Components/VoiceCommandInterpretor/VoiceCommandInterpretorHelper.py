import whisper
from transformers import pipeline

speech_model = whisper.load_model("base")
intent_classifier = pipeline("zero-shot-classification")

INTENT_LABELS = [
    "run shell command",
    "open app",
    "search web",
    "summarize",
    "transcribe",
    "read aloud",
    "file operation",
    "send email",
    "unknown"
]

def transcribe_voice(file_path: str) -> str:
    result = speech_model.transcribe(file_path)
    return result["text"].strip()

def classify_voice_intent(text: str) -> str:
    result = intent_classifier(text, INTENT_LABELS)
    return result['labels'][0]

def interpret_voice_command(file_path: str) -> dict:
    try:
        transcript = transcribe_voice(file_path)
        intent = classify_voice_intent(transcript)
        return {
            "transcript": transcript,
            "intent": intent
        }
    except Exception as e:
        return {
            "error": str(e)
        }