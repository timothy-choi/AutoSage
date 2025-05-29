from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TextToSpeechHelper import speak_text, save_speech, set_voice

router = APIRouter()

class TextInput(BaseModel):
    text: str

class SaveSpeechInput(BaseModel):
    text: str
    filename: str = "output.mp3"

class SetVoiceInput(BaseModel):
    voice_name: str

@router.post("/tts/speak")
def speak_endpoint(data: TextInput):
    try:
        speak_text(data.text)
        return {"status": "spoken"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts/save")
def save_endpoint(data: SaveSpeechInput):
    try:
        save_speech(data.text, data.filename)
        return {"status": "saved", "filename": data.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tts/set_voice")
def set_voice_endpoint(data: SetVoiceInput):
    try:
        success = set_voice(data.voice_name)
        if success:
            return {"status": "voice set", "voice": data.voice_name}
        else:
            raise HTTPException(status_code=404, detail="Voice not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))