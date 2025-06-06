from googletrans import Translator
from typing import List

translator = Translator()

def translate_text(text: str, dest_lang: str = "en", src_lang: str = "auto") -> dict:
    result = translator.translate(text, src=src_lang, dest=dest_lang)
    return {
        "source_language": result.src,
        "translated_text": result.text,
        "detected_language": result.src
    }

def detect_language(text: str) -> dict:
    detection = translator.detect(text)
    return {
        "language": detection.lang,
        "confidence": detection.confidence
    }

def batch_translate(texts: List[str], dest_lang: str = "en", src_lang: str = "auto") -> List[dict]:
    results = translator.translate(texts, src=src_lang, dest=dest_lang)
    return [
        {
            "original_text": result.origin,
            "translated_text": result.text,
            "source_language": result.src
        }
        for result in results
    ]

def supported_languages() -> List[str]:
    return list(translator.LANGUAGES.keys())