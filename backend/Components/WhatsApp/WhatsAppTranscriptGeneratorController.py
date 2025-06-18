from fastapi import APIRouter, HTTPException
from WhatsAppTranscriptGeneratorHelper import (
    store_whatsapp_message,
    get_transcript_by_user
)

router = APIRouter()

@router.post("/whatsapp/transcript/store")
def store_transcript(data: dict):
    try:
        store_whatsapp_message(data)
        return {"status": "stored"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/whatsapp/transcript/user/{whatsapp_number}")
def get_user_transcript(whatsapp_number: str):
    try:
        messages = get_transcript_by_user(whatsapp_number)
        return {"user": whatsapp_number, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))