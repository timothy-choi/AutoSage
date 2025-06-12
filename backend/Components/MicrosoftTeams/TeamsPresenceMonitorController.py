from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TeamsPresenceMonitorHelper import (
    fetch_user_presence,
    batch_fetch_presence,
    fetch_presence_with_timestamp,
    fetch_filtered_presence
)

router = APIRouter()

class PresenceRequest(BaseModel):
    graph_api_url: str
    user_id: str
    access_token: str

class BatchPresenceRequest(BaseModel):
    graph_api_url: str
    user_ids: List[str]
    access_token: str

class FilteredPresenceRequest(BaseModel):
    graph_api_url: str
    user_ids: List[str]
    status_filter: List[str]
    access_token: str

@router.post("/teams/get-user-presence")
async def get_user_presence(req: PresenceRequest):
    result = await fetch_user_presence(req.graph_api_url, req.user_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/get-batch-presence")
async def get_batch_presence(req: BatchPresenceRequest):
    result = await batch_fetch_presence(req.graph_api_url, req.user_ids, req.access_token)
    return result

@router.post("/teams/get-presence-with-timestamp")
async def get_presence_with_timestamp(req: PresenceRequest):
    result = await fetch_presence_with_timestamp(req.graph_api_url, req.user_id, req.access_token)
    return result

@router.post("/teams/get-filtered-presence")
async def get_filtered_presence(req: FilteredPresenceRequest):
    result = await fetch_filtered_presence(req.graph_api_url, req.user_ids, req.access_token, req.status_filter)
    return result