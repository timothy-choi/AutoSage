from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsMessageCleanerHelper import (
    delete_teams_message,
    bulk_delete_old_messages
)

router = APIRouter()

class DeleteMessageRequest(BaseModel):
    teams_base_url: str
    team_id: str
    channel_id: str
    message_id: str
    access_token: str

class BulkDeleteRequest(BaseModel):
    teams_base_url: str
    team_id: str
    channel_id: str
    days_old: int
    access_token: str

@router.post("/teams/delete-message")
async def delete_message(req: DeleteMessageRequest):
    result = await delete_teams_message(
        req.teams_base_url,
        req.team_id,
        req.channel_id,
        req.message_id,
        req.access_token
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/bulk-delete-messages")
async def bulk_delete(req: BulkDeleteRequest):
    result = await bulk_delete_old_messages(
        req.teams_base_url,
        req.team_id,
        req.channel_id,
        req.days_old,
        req.access_token
    )
    return result