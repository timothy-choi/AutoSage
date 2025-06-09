from fastapi import APIRouter, Query, HTTPException, Body
from typing import Dict

from TeamsThreadReplierHelper import (
    reply_to_thread_message,
    reply_with_markdown,
    reply_with_mention
)

router = APIRouter()


@router.post("/teams/thread/reply")
def plain_thread_reply(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    parent_message_id: str = Query(...),
    reply_text: str = Query(...)
):
    try:
        result = reply_to_thread_message(access_token, team_id, channel_id, parent_message_id, reply_text)
        return {"status": "replied", "reply_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/thread/reply/markdown")
def markdown_thread_reply(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    parent_message_id: str = Query(...),
    markdown: str = Query(...)
):
    try:
        result = reply_with_markdown(access_token, team_id, channel_id, parent_message_id, markdown)
        return {"status": "replied", "reply_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/thread/reply/mention")
def mention_thread_reply(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    parent_message_id: str = Query(...),
    user_id: str = Query(...),
    display_name: str = Query(...),
    message: str = Query(...)
):
    try:
        result = reply_with_mention(access_token, team_id, channel_id, parent_message_id, user_id, display_name, message)
        return {"status": "replied", "reply_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))