from fastapi import APIRouter, UploadFile, File, HTTPException
from VoiceToTextHelper import transcribe_audio, detect_language, transcribe_with_timestamps
import tempfile

router = APIRouter()

@router.post("/voice/transcribe")
async def transcribe(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        result = transcribe_audio(tmp_path)
        return {"transcript": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/language")
async def detect(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        language = detect_language(tmp_path)
        return {"language": language}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/timestamps")
async def transcribe_with_time(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name
        segments = transcribe_with_timestamps(tmp_path)
        return {"segments": segments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))