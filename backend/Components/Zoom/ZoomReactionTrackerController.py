from fastapi import APIRouter, Request, Header, Query
from typing import Optional
from zoom_reaction_tracker_helper import (
    parse_reaction_event,
    is_reaction_allowed,
    is_email_domain_allowed,
    format_human_time,
    forward_reaction_to_webhook,
    REACTION_EMOJIS
)

router = APIRouter()

@router.post("/zoom/webhook/reaction")
async def zoom_reaction_webhook(
    request: Request,
    x_zm_request_timestamp: str = Header(...),
    x_zm_signature: str = Header(...),
    webhook_url: Optional[str] = Query(None, description="Optional endpoint to forward the reaction"),
    allowed_domains: Optional[str] = Query(None, description="Comma-separated allowed domains (e.g., yourco.com)")
):
    """
    Handles Zoom reaction events and optionally forwards them to a webhook.
    Fully stateless.
    """
    try:
        payload = await request.json()
        event = payload.get("event")

        if event != "meeting.reaction_sent":
            return {"status": "ignored", "reason": f"event {event} not supported"}

        data = parse_reaction_event(payload)

        if not is_reaction_allowed(data["reaction_type"]):
            return {"status": "ignored", "reason": "reaction type not allowed"}

        if allowed_domains:
            allowed_list = [d.strip() for d in allowed_domains.split(",")]
            if not is_email_domain_allowed(data["email"], allowed_list):
                return {"status": "ignored", "reason": "email domain not allowed"}

        emoji = REACTION_EMOJIS.get(data["reaction_type"], "❓")
        human_time = format_human_time(data["timestamp"])

        enhanced_data = {
            "reaction": data["reaction_type"],
            "emoji": emoji,
            "participant": data["participant_name"],
            "email": data["email"],
            "meeting_id": data["meeting_id"],
            "timestamp": data["timestamp"],
            "time_human": human_time,
            "message": f"{data['participant_name']} reacted with {emoji} at {human_time}"
        }

        if webhook_url:
            forward_result = forward_reaction_to_webhook(enhanced_data, webhook_url)
            return {
                "status": "forwarded",
                "reaction": enhanced_data,
                "forward_result": forward_result
            }

        return {"status": "received", "reaction": enhanced_data}

    except Exception as e:
        return {"error": str(e)}
