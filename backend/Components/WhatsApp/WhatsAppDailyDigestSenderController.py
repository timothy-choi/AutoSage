from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from WhatsAppDailyDigestSenderHelper import (
    load_recent_messages,
    compile_digest,
    send_digest
)

router = APIRouter()

class DigestRequestPayload(BaseModel):
    to: str
    hours: int = 24

@router.post("/whatsapp/digest/send")
def send_daily_digest(payload: DigestRequestPayload):
    try:
        messages = load_recent_messages(within_hours=payload.hours)
        digest = compile_digest(messages)
        sid = send_digest(payload.to, digest)
        return {"status": "sent", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))