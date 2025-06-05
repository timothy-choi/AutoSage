from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from SMSNotifierHelper import send_sms
import os

router = APIRouter()

class SMSRequest(BaseModel):
    account_sid: str
    auth_token: str
    from_number: str
    to_number: str
    message: str

@router.post("/notify/sms")
def send_sms_notification(data: SMSRequest):
    try:
        sid = send_sms(
            account_sid=data.account_sid,
            auth_token=data.auth_token,
            from_number=data.from_number,
            to_number=data.to_number,
            message=data.message
        )
        return {"message": "SMS sent successfully", "sid": sid}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))