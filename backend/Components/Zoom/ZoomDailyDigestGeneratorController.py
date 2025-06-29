from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from zoom_daily_digest_generator_helper import (
    fetch_daily_meetings,
    generate_daily_digest
)

router = APIRouter()

class ZoomDailyDigestRequest(BaseModel):
    user_id: str = Field(..., description="Zoom user ID (e.g. 'me')")
    jwt_token: str = Field(..., description="Zoom JWT token")
    date: str = Field(..., description="Date in ISO format (e.g. 2025-06-23)")

@router.post("/zoom/daily-digest")
def zoom_daily_digest(request: ZoomDailyDigestRequest):
    try:
        meetings = fetch_daily_meetings(request.user_id, request.jwt_token, request.date)
        digest = generate_daily_digest(meetings, request.date)
        return {"digest": digest}
    except Exception as e:
