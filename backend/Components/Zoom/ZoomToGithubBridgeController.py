from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Literal
from ZoomToGithubBridgeHelper import sync_zoom_meetings_to_github

router = APIRouter()

class ZoomToGitHubRequest(BaseModel):
    user_id: str = Field(..., description="Zoom user ID (e.g. 'me')")
    jwt_token: str = Field(..., description="Zoom JWT token")
    github_token: str = Field(..., description="GitHub personal access token with repo access")
    repo_owner: str = Field(..., description="GitHub repo owner (username or org)")
    repo_name: str = Field(..., description="GitHub repository name")
    meeting_type: Literal["past", "upcoming"] = "past"

@router.post("/zoom/sync-to-github")
def zoom_to_github_bridge(request: ZoomToGitHubRequest):
    try:
        results = sync_zoom_meetings_to_github(
            user_id=request.user_id,
            jwt_token=request.jwt_token,
            repo_owner=request.repo_owner,
            repo_name=request.repo_name,
            github_token=request.github_token,
            meeting_type=request.meeting_type
        )
        return {"synced": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))