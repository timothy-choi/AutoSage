from fastapi import APIRouter, Request
from TwitchWebhookListenerHelper import handle_twitch_event

router = APIRouter()

@router.post("/webhooks/twitch")
async def twitch_webhook_listener(request: Request):
    return await handle_twitch_event(request)