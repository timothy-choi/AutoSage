from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from SlackDMStarterHelper import open_dm_channel, send_dm_message

router = APIRouter()

class DMRequest(BaseModel):
    token: str
    user_id: str
    message: str

@router.post("/slack/start-dm")
def start_dm_conversation(data: DMRequest):
    try:
        channel_id = open_dm_channel(data.token, data.user_id)
        result = send_dm_message(data.token, channel_id, data.message)

        if not result.get("ok"):
            raise HTTPException(status_code=400, detail=result.get("error", "Failed to send message"))

        return {
            "message": "DM sent successfully",
            "channel_id": channel_id,
            "ts": result.get("ts")
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))