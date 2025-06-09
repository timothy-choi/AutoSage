from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional
from TeamsMessageSenderHelper import (
    send_teams_message,
    send_markdown_message,
    reply_to_channel_message,
    send_mention_message,
    send_adaptive_card,
)

router = APIRouter()


@router.post("/teams/send")
def post_teams_message(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    message: str = Query(...)
):
    try:
        result = send_teams_message(access_token, team_id, channel_id, message)
        return {"status": "sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/send/markdown")
def post_markdown_message(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    markdown: str = Query(...)
):
    try:
        result = send_markdown_message(access_token, team_id, channel_id, markdown)
        return {"status": "sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/reply")
def reply_to_message(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    parent_message_id: str = Query(...),
    reply_text: str = Query(...)
):
    try:
        result = reply_to_channel_message(access_token, team_id, channel_id, parent_message_id, reply_text)
        return {"status": "replied", "reply_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/mention")
def mention_user(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    user_id: str = Query(...),
    display_name: str = Query(...),
    message: str = Query(...)
):
    try:
        result = send_mention_message(access_token, team_id, channel_id, user_id, display_name, message)
        return {"status": "sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/teams/adaptive-card")
def post_adaptive_card(
    access_token: str = Query(...),
    team_id: str = Query(...),
    channel_id: str = Query(...),
    card_json: dict = Body(...)
):
    try:
        result = send_adaptive_card(access_token, team_id, channel_id, card_json)
        return {"status": "card_sent", "message_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))