from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from WhatsAppBulkMessengerHelper import send_bulk_whatsapp_messages

router = APIRouter()

class BulkMessagePayload(BaseModel):
    to: List[str]
    message: str

@router.post("/whatsapp/send-bulk")
def send_bulk(payload: BulkMessagePayload):
    if not payload.to:
        raise HTTPException(status_code=400, detail="Recipient list is empty.")
    
    try:
        results = send_bulk_whatsapp_messages(payload.to, payload.message)
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))