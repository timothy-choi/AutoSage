from fastapi import APIRouter, UploadFile, File, HTTPException
from VoiceCommandInterpretorHelper import interpret_voice_command, transcribe_voice, classify_voice_intent
import tempfile
from pydantic import BaseModel

class TextInput(BaseModel):
    text: str

router = APIRouter()

@router.post("/voice/interpret")
async def interpret_voice(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        result = interpret_voice_command(tmp_path)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/transcribe")
async def transcribe_voice_only(file: UploadFile = File(...)):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
            tmp.write(await file.read())
            tmp_path = tmp.name

        transcript = transcribe_voice(tmp_path)
        return {"transcript": transcript}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/voice/classify")
async def classify_text(data: TextInput):
    try:
        intent = classify_voice_intent(data.text)
        return {"intent": intent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
