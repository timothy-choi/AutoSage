from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditDownvoterHelper import downvote_item

router = APIRouter()

class RedditDownvoteRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditDownvoter/0.1 by YourBot")
    item_id: str 

@router.post("/reddit/downvote")
def reddit_downvote(request: RedditDownvoteRequest):
    try:
        result = downvote_item(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            item_id=request.item_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))