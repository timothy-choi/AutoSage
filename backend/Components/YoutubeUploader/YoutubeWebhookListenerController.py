from fastapi import APIRouter, Request, Response
from fastapi.responses import PlainTextResponse
from YotuubeWebhookListenerHelper import handle_youtube_verification, parse_youtube_notification

router = APIRouter()

@router.get("/youtube/webhook")
async def youtube_webhook_get(request: Request):
    result = handle_youtube_verification(request)
    challenge = result.get("challenge")
    if challenge:
        return PlainTextResponse(content=challenge)
    return result

@router.post("/youtube/webhook")
async def youtube_webhook_post(request: Request):
    body = await request.body()
    xml_str = body.decode("utf-8")
    parsed = parse_youtube_notification(xml_str)
    return parsed