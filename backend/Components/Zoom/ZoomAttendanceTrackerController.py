from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from ZoomAttendanceTrackerHelper import (
    fetch_zoom_attendance,
    format_attendance_report
)

router = APIRouter()

class ZoomAttendanceRequest(BaseModel):
    meeting_id: str = Field(..., description="Zoom meeting ID")
    jwt_token: str = Field(..., description="Zoom JWT token")
    timezone: str = Field(default="UTC", description="Timezone for timestamps (e.g., 'America/Los_Angeles')")

@router.post("/zoom/attendance-report")
def generate_attendance_report(request: ZoomAttendanceRequest):
    try:
        participants = fetch_zoom_attendance(request.meeting_id, request.jwt_token)
        report = format_attendance_report(participants, request.timezone)
        return {"report": report, "total_participants": len(report)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))