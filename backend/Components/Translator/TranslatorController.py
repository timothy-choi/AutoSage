from fastapi import APIRouter, Query, HTTPException
from TranslatorHelper import translate_text, detect_language, batch_translate, supported_languages

router = APIRouter()

@router.get("/translate")
def translate(
    text: str = Query(..., description="Text to translate"),
    to: str = Query("en", description="Target language code (e.g., 'en', 'fr')"),
    from_lang: str = Query("auto", description="Source language code")
):
    try:
        result = translate_text(text, dest_lang=to, src_lang=from_lang)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/translate/detect")
def detect(text: str):
    return detect_language(text)

@router.post("/translate/batch")
def batch_translate_endpoint(texts: List[str], to: str = "en", from_lang: str = "auto"):
    return batch_translate(texts, dest_lang=to, src_lang=from_lang)

@router.get("/translate/supported")
def get_supported_languages():
    return {"languages": supported_languages()}