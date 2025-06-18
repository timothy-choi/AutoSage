from fastapi import Request, HTTPException
import hmac
import hashlib
import base64

TWITCH_SECRET = "your_shared_secret"

async def verify_twitch_signature(request: Request) -> bool:
    received_sig = request.headers.get("Twitch-Eventsub-Message-Signature")
    message_id = request.headers.get("Twitch-Eventsub-Message-Id")
    timestamp = request.headers.get("Twitch-Eventsub-Message-Timestamp")
    body = (await request.body()).decode()

    if not received_sig or not message_id or not timestamp:
        return False

    hmac_message = message_id + timestamp + body
    hmac_hash = hmac.new(TWITCH_SECRET.encode(), hmac_message.encode(), hashlib.sha256).hexdigest()
    expected_sig = f"sha256={hmac_hash}"

    return hmac.compare_digest(received_sig, expected_sig)


async def handle_twitch_event(request: Request) -> dict:
    if not await verify_twitch_signature(request):
        raise HTTPException(status_code=403, detail="Invalid Twitch signature")

    payload = await request.json()
    event_type = request.headers.get("Twitch-Eventsub-Message-Type")

    if event_type == "webhook_callback_verification":
        return {"challenge": payload["challenge"]}

    elif event_type == "notification":
        event = payload.get("event")

        print(f"Received Twitch Event: {event}")

    return {"status": "ok"}