from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditSubredditSubscriberHelper import subscribe_to_subreddit

router = APIRouter()

class RedditSubredditSubscribeRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditSubredditSubscriber/0.1 by YourBot")
    subreddit_name: str

@router.post("/reddit/subscribe")
def reddit_subscribe(request: RedditSubredditSubscribeRequest):
    try:
        result = subscribe_to_subreddit(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            subreddit_name=request.subreddit_name
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))