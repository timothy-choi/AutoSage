from fastapi import APIRouter, Request, Header
from ZoomParticipantJoinWatcherHelper import parse_participant_joined
import logging
import os

router = APIRouter()

ZOOM_WEBHOOK_SECRET = os.getenv("ZOOM_WEBHOOK_SECRET", "")

@router.post("/zoom/webhook/participant-joined")
async def zoom_participant_joined_webhook(
    request: Request,
    x_zm_request_timestamp: str = Header(...),
    x_zm_signature: str = Header(...)
):
    try:
        payload = await request.json()

        event = payload.get("event")
        if event != "meeting.participant_joined":
            return {"message": f"Ignored event: {event}"}

        info = parse_participant_joined(payload)

        logging.info(f"Participant joined: {info}")
        
        return {"status": "received", "participant": info}

    except Exception as e:
        return {"error": str(e)}