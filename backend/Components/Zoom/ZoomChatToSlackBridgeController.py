from fastapi import APIRouter, Request, Header, Body
from typing import List, Dict, Optional
from ZoomChatToSlackBridgeHelper import forward_zoom_chat_to_slack, should_forward_message

router = APIRouter()

@router.post("/zoom/webhook/chat-to-slack")
async def zoom_chat_to_slack_stateless(
    request: Request,
    slack_webhook_url: str = Header(..., description="Slack webhook URL to post messages to"),
    allowed_domains: Optional[str] = Header(None, description="Comma-separated list of allowed sender domains"),
    keywords: Optional[str] = Header(None, description="Comma-separated keyword list to filter messages"),
    allow_group: Optional[bool] = Header(False, description="Allow group messages (default false)"),
    user_map: Optional[Dict[str, str]] = Body(default=None, description="Optional sender email to Slack tag mapping")
):
    """
    Stateless Zoom to Slack chat bridge.
    Pass all routing and filtering via headers/body per request.
    """
    try:
        payload = await request.json()
        event = payload.get("event")
        if event != "chat.message.sent":
            return {"message": f"Ignored event: {event}"}

        obj = payload["payload"]["object"]
        sender = obj.get("sender", {})
        sender_name = sender.get("user_name", "Unknown")
        sender_email = sender.get("email", "")
        message = obj.get("message", "")
        chat_type = obj.get("chat_type", "1on1")
        timestamp = obj.get("date_time", "")

        allowed_domain_list = [d.strip() for d in allowed_domains.split(",")] if allowed_domains else []
        keyword_list = [k.strip() for k in keywords.split(",")] if keywords else []

        should_send, reason = should_forward_message(
            sender_email=sender_email,
            chat_type=chat_type,
            message=message,
            allowed_domains=allowed_domain_list,
            keywords=keyword_list,
            allow_group=allow_group
        )

        if not should_send:
            return {"status": "skipped", "reason": reason}

        result = forward_zoom_chat_to_slack(
            slack_webhook_url=slack_webhook_url,
            sender_name=sender_name,
            sender_email=sender_email,
            message=message,
            timestamp=timestamp,
            user_map=user_map
        )

        return {"status": "forwarded", "slack_result": result}

    except Exception as e:
        return {"error": str(e)}