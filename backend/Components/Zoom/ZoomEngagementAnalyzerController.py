from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ZoomEngagementAnalyzerHelper import generate_zoom_engagement_report

router = APIRouter()

class ZoomEngagementRequest(BaseModel):
    meeting_id: str = Field(..., description="Zoom meeting ID")
    jwt_token: str = Field(..., description="Zoom JWT token")

@router.post("/zoom/engagement-score")
def get_engagement_score(request: ZoomEngagementRequest):
    try:
        result = generate_zoom_engagement_report(
            meeting_id=request.meeting_id,
            jwt_token=request.jwt_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))