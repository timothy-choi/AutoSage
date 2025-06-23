from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from LinkedinPostSchedulerHelper import schedule_linkedin_message

router = APIRouter()

class LinkedInScheduledMessageRequest(BaseModel):
    access_token: str = Field(..., description="LinkedIn OAuth2 access token")
    author_urn: str = Field(..., description="URN of the recipient (e.g., 'urn:li:person:xxxx')")
    message_text: str = Field(..., description="Message content")
    scheduled_time: int = Field(..., description="Unix timestamp (seconds) when message should be sent")

@router.post("/linkedin/schedule-message")
def schedule_message(request: LinkedInScheduledMessageRequest, background_tasks: BackgroundTasks):
    now = int(datetime.utcnow().timestamp())
    if request.scheduled_time <= now:
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")

    background_tasks.add_task(
        schedule_linkedin_message,
        request.access_token,
        request.author_urn,
        request.message_text,
        request.scheduled_time
    )

    return {
        "status": "scheduled",
        "message": f"Message will be sent at {datetime.utcfromtimestamp(request.scheduled_time)} UTC"
    }