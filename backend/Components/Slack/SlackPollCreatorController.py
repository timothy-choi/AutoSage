from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from SlackPollCreatorHelper import create_slack_poll

router = APIRouter()

class PollRequest(BaseModel):
    token: str
    channel: str
    question: str
    options: List[str]

@router.post("/slack/create-poll")
def slack_create_poll(data: PollRequest):
    try:
        if len(data.options) < 2:
            raise HTTPException(status_code=400, detail="At least two options are required for a poll.")

        response = create_slack_poll(data.token, data.channel, data.question, data.options)

        if not response.get("ok"):
            raise HTTPException(status_code=400, detail=response.get("error", "Slack API error"))

        return {
            "message": "Poll posted successfully",
            "channel": data.channel,
            "question": data.question,
            "options": data.options,
            "ts": response.get("ts")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))