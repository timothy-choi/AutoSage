from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookMessageSchedulerHelper import schedule_facebook_message

router = APIRouter()

class FacebookSchedulePayload(BaseModel):
    recipient_id: str
    message: str
    send_time: str  

@router.post("/facebook/schedule")
def schedule_facebook_msg(payload: FacebookSchedulePayload):
    try:
        result = schedule_facebook_message(payload.recipient_id, payload.message, payload.send_time)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))