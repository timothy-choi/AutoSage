from fastapi import APIRouter
from pydantic import BaseModel
from FigmaActivityTrackerHelper import fetch_figma_activity

router = APIRouter()

class FigmaActivityRequest(BaseModel):
    access_token: str
    team_id: str

@router.post("/figma/activity-log")
def get_figma_activity_log(request: FigmaActivityRequest):
    return fetch_figma_activity(
        access_token=request.access_token,
        team_id=request.team_id
    )