from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from DiscordPollCreatorHelper import create_poll, close_poll, get_poll_results, delete_poll

router = APIRouter()

class PollRequest(BaseModel):
    channel_id: int
    question: str
    options: List[str]

class ClosePollRequest(BaseModel):
    channel_id: int
    message_id: int
    note: str = "\U0001F6D1 Poll Closed"

class PollResultRequest(BaseModel):
    channel_id: int
    message_id: int

class DeletePollRequest(BaseModel):
    channel_id: int
    message_id: int

@router.post("/discord/create-poll")
async def create_discord_poll(req: PollRequest):
    from bot_runner import bot
    if not bot.is_ready():
        raise HTTPException(status_code=503, detail="Bot is not ready")

    response = await create_poll(bot, req.channel_id, req.question, req.options)
    return {"status": "success", "message": response}

@router.post("/discord/close-poll")
async def close_poll_api(req: ClosePollRequest):
    from bot_runner import bot
    result = await close_poll(bot, req.channel_id, req.message_id, req.note)
    return {"result": result}

@router.post("/discord/poll-results")
async def get_poll_results_api(req: PollResultRequest):
    from bot_runner import bot
    results = await get_poll_results(bot, req.channel_id, req.message_id)
    return results

@router.post("/discord/delete-poll")
async def delete_poll_api(req: DeletePollRequest):
    from bot_runner import bot
    result = await delete_poll(bot, req.channel_id, req.message_id)
    return {"result": result}