from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from DropBoxTeamActivityFetcherHelper import fetch_dropbox_team_activity

router = APIRouter()

class DropboxTeamActivityRequest(BaseModel):
    team_access_token: str = Field(..., description="Dropbox Business team access token")
    start_time: Optional[str] = Field(None, description="Start time (ISO 8601)")
    end_time: Optional[str] = Field(None, description="End time (ISO 8601)")
    limit: Optional[int] = Field(100, description="Max number of events (default 100)")

@router.post("/dropbox/team/activity")
def get_dropbox_team_activity(request: DropboxTeamActivityRequest):
    try:
        logs = fetch_dropbox_team_activity(
            team_access_token=request.team_access_token,
            start_time=request.start_time,
            end_time=request.end_time,
            limit=request.limit
        )
        return {
            "event_count": len(logs),
            "events": logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))