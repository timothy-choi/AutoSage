from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookMessageSenderHelper import send_facebook_message

router = APIRouter()

class FacebookMessagePayload(BaseModel):
    recipient_id: str 
    message: str

@router.post("/facebook/send")
def send_facebook_msg(payload: FacebookMessagePayload):
    try:
        result = send_facebook_message(payload.recipient_id, payload.message)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))