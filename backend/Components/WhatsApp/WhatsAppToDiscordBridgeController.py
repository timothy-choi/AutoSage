from fastapi import APIRouter, Request, HTTPException
from WhatsAppToDiscordBridgeHelper import forward_to_discord

router = APIRouter()

@router.post("/whatsapp/bridge/discord")
async def bridge_whatsapp_to_discord(request: Request):
    try:
        form = await request.form()
        whatsapp_data = {
            "from": form.get("From"),
            "to": form.get("To"),
            "message_body": form.get("Body"),
            "timestamp": form.get("Timestamp"),
            "profile_name": form.get("ProfileName"),
            "wa_id": form.get("WaId")
        }

        status = forward_to_discord(whatsapp_data)
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))