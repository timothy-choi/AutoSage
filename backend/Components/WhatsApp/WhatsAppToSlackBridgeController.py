from fastapi import APIRouter, Request, HTTPException
from WhatsAppToSlackBridgeHelper import forward_to_slack

router = APIRouter()

@router.post("/whatsapp/bridge/slack")
async def bridge_whatsapp_to_slack(request: Request):
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

        status = forward_to_slack(whatsapp_data)
        return {"status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))