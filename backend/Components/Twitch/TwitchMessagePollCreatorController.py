from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from TwitchMessagePollCreatorHelper import create_twitch_poll, end_twitch_poll, get_active_twitch_polls

router = APIRouter()

class TwitchPollRequest(BaseModel):
    oauth_token: str
    client_id: str
    broadcaster_id: str
    title: str
    choices: List[str]
    duration: int

class EndPollRequest(BaseModel):
    oauth_token: str
    client_id: str
    poll_id: str
    broadcaster_id: str

class ActivePollsRequest(BaseModel):
    oauth_token: str
    client_id: str
    broadcaster_id: str

@router.post("/twitch/create-poll")
async def create_poll(req: TwitchPollRequest):
    result = await create_twitch_poll(
        req.oauth_token, req.client_id, req.broadcaster_id, req.title, req.choices, req.duration
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.patch("/twitch/end-poll")
async def end_poll(req: EndPollRequest):
    result = await end_twitch_poll(req.oauth_token, req.client_id, req.poll_id, req.broadcaster_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.get("/twitch/active-polls")
async def get_polls(oauth_token: str, client_id: str, broadcaster_id: str):
    result = await get_active_twitch_polls(oauth_token, client_id, broadcaster_id)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result