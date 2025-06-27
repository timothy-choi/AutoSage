from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ZoomMeetingSummaryGeneratorHelper import (
    fetch_zoom_meeting_details,
    fetch_zoom_meeting_participants,
    generate_meeting_summary
)

router = APIRouter()

class ZoomSummaryRequest(BaseModel):
    meeting_id: str = Field(..., description="Zoom meeting ID")
    jwt_token: str = Field(..., description="Zoom JWT token")

@router.post("/zoom/generate-summary")
def generate_zoom_summary(request: ZoomSummaryRequest):
    try:
        meeting_data = fetch_zoom_meeting_details(request.meeting_id, request.jwt_token)
        participants = fetch_zoom_meeting_participants(request.meeting_id, request.jwt_token)
        summary = generate_meeting_summary(meeting_data, participants)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))