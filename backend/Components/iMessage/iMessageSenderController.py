from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from iMessageSenderHelper import send_imessage

router = APIRouter()

class IMessageRequest(BaseModel):
    recipient: str  
    message: str
    group: bool = False

@router.post("/notify/imessage")
def send_imessage_notification(data: IMessageRequest):
    try:
        result = send_imessage(data.recipient, data.message, data.group)
        return {"message": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))