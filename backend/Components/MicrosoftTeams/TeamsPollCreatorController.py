from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TeamsPollCreatorHelper import create_teams_poll

router = APIRouter()

class TeamsPollRequest(BaseModel):
    webhook_url: str
    question: str
    options: List[str]

@router.post("/teams/create-poll")
async def create_teams_poll_api(req: TeamsPollRequest):
    result = await create_teams_poll(req.webhook_url, req.question, req.options)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result