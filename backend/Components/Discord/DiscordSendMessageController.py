from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from DiscordSendMessageHelper import send_discord_message, send_embed

router = APIRouter()

@router.post("/discord/send")
def post_discord_message(
    token: str = Query(..., description="Bot token starting with 'Bot '"),
    channel_id: str = Query(..., description="Target Discord channel ID"),
    message: str = Query(..., description="Message content"),
    reply_to: Optional[str] = Query(None, description="Message ID to reply to"),
    mention_users: Optional[List[str]] = Query(None, description="User IDs to mention"),
    mention_roles: Optional[List[str]] = Query(None, description="Role IDs to mention")
):
    try:
        result = send_discord_message(token, channel_id, message, reply_to, mention_users, mention_roles)
        return {"status": "sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/embed")
def post_discord_embed(
    token: str = Query(...),
    channel_id: str = Query(...),
    title: str = Query(...),
    description: str = Query(...),
    color: int = Query(0x5865F2)
):
    try:
        result = send_embed(token, channel_id, title, description, color)
        return {"status": "embed_sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))