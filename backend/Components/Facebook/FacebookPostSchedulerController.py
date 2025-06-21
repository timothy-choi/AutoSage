from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from FacebookPostSchedulerHelper import (
    schedule_text_post,
    schedule_photo_post
)

router = APIRouter()

class FacebookTextSchedulePayload(BaseModel):
    message: str
    scheduled_time: str

class FacebookPhotoSchedulePayload(BaseModel):
    image_url: str
    caption: str
    scheduled_time: str

@router.post("/facebook/schedule/text")
def schedule_text(payload: FacebookTextSchedulePayload):
    try:
        result = schedule_text_post(payload.message, payload.scheduled_time)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/facebook/schedule/photo")
def schedule_photo(payload: FacebookPhotoSchedulePayload):
    try:
        result = schedule_photo_post(payload.image_url, payload.caption, payload.scheduled_time)
        return {"status": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))