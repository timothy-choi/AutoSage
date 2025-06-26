from fastapi import APIRouter, Query
from ZoomChatMessageSenderHelper import send_zoom_chat_message

router = APIRouter()

@router.post("/zoom/chat/send")
def send_zoom_chat(
    access_token: str = Query(..., description="Zoom OAuth access token"),
    to_jid: str = Query(..., description="JID of user or channel"),
    message: str = Query(..., description="Message text to send"),
    is_channel: bool = Query(False, description="Is this a channel message?")
):
    try:
        result = send_zoom_chat_message(access_token, to_jid, message, is_channel)
        return result
    except Exception as e:
        return {"error": str(e)}