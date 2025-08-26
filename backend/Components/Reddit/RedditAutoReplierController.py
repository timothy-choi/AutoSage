from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditAutoReplierHelper import auto_reply_to_item

router = APIRouter()

class RedditAutoReplyRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditAutoReplier/0.1 by YourBot")
    item_id: str  
    reply_text: str

@router.post("/reddit/auto-reply")
def reddit_auto_reply(request: RedditAutoReplyRequest):
    try:
        result = auto_reply_to_item(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            item_id=request.item_id,
            reply_text=request.reply_text
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))