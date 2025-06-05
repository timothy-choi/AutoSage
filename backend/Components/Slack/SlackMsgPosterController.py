from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from SlackMsgPosterHelper import post_slack_message

router = APIRouter()

class SlackTokenMessage(BaseModel):
    token: str
    channel: str
    message: str

@router.post("/slack/send-token")
def send_token_message(data: SlackTokenMessage):
    result = post_slack_message(data.token, data.channel, data.message)

    if not result.get("ok"):
        raise HTTPException(status_code=400, detail=result.get("error"))

    return {
        "message": "Message sent successfully",
        "channel": data.channel,
        "response": result
    }