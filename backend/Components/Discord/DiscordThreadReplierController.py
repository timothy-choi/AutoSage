from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
from DiscordThreadReplierHelper import (
    send_plain_reply,
    send_markdown_reply,
    send_embed_reply,
    send_mentions_reply
)

router = APIRouter()

@router.post("/discord/thread/reply/plain")
def post_plain_reply(
    token: str = Query(...),
    thread_id: str = Query(...),
    message: str = Query(...)
):
    try:
        return send_plain_reply(token, thread_id, message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/thread/reply/markdown")
def post_markdown_reply(
    token: str = Query(...),
    thread_id: str = Query(...),
    message: str = Query(...),
    bold: bool = Query(False),
    italic: bool = Query(False),
    underline: bool = Query(False),
    code: bool = Query(False)
):
    try:
        return send_markdown_reply(token, thread_id, message, bold, italic, underline, code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/thread/reply/embed")
def post_embed_reply(
    token: str = Query(...),
    thread_id: str = Query(...),
    title: str = Query(...),
    description: str = Query(...),
    color: int = Query(0x5865F2)
):
    try:
        return send_embed_reply(token, thread_id, title, description, color)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/discord/thread/reply/mentions")
def post_mentions_reply(
    token: str = Query(...),
    thread_id: str = Query(...),
    message: str = Query(...),
    user_ids: Optional[List[str]] = Query(None),
    role_ids: Optional[List[str]] = Query(None)
):
    try:
        return send_mentions_reply(token, thread_id, message, user_ids, role_ids)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))