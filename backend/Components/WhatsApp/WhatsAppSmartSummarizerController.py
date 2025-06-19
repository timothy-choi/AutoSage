from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from WhatsAppSmartSummaryGeneratorHelper import (
    load_messages_for_summary,
    generate_basic_summary
)

router = APIRouter()

class SummaryRequestPayload(BaseModel):
    hours: int = 24

@router.post("/whatsapp/summary/generate")
def generate_summary(payload: SummaryRequestPayload):
    try:
        messages = load_messages_for_summary(payload.hours)
        summary = generate_basic_summary(messages)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))