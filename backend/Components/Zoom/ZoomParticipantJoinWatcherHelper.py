import hmac
import hashlib
import base64
import json
from fastapi import Request

async def verify_zoom_webhook(request: Request, secret_token: str):
    message = f"{request.headers['x-zm-request-timestamp']}{await request.body()}"
    signature = hmac.new(
        secret_token.encode(),
        message.encode(),
        hashlib.sha256
    ).digest()
    computed_signature = f"v0={base64.b64encode(signature).decode()}"

    return hmac.compare_digest(computed_signature, request.headers.get("x-zm-signature", ""))
    
def parse_participant_joined(payload: dict):
    return {
        "meeting_id": payload.get("payload", {}).get("object", {}).get("id"),
        "participant_user_id": payload.get("payload", {}).get("object", {}).get("participant", {}).get("user_id"),
        "participant_name": payload.get("payload", {}).get("object", {}).get("participant", {}).get("user_name"),
        "join_time": payload.get("payload", {}).get("object", {}).get("participant", {}).get("join_time"),
        "email": payload.get("payload", {}).get("object", {}).get("participant", {}).get("email", "")
    }