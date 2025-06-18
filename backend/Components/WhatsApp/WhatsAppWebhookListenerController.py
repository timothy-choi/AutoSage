from fastapi import APIRouter, Request
from WhatsAppWebhookListenerHelper import (
    parse_whatsapp_webhook,
    handle_media_messages,
    handle_location_messages,
    auto_reply_to_keywords,
    log_incoming_message,
)

router = APIRouter()

@router.post("/whatsapp/webhook/listen")
async def whatsapp_webhook_listener(request: Request):
    form = await request.form()
    parsed_data = parse_whatsapp_webhook(form)

    log_incoming_message(parsed_data)

    response_payload = {
        "status": "received",
        "from": parsed_data["from"],
        "message": parsed_data["message_body"]
    }

    media = handle_media_messages(parsed_data)
    if media:
        response_payload["media"] = media

    location = handle_location_messages(parsed_data)
    if location:
        response_payload["location"] = location

    return response_payload