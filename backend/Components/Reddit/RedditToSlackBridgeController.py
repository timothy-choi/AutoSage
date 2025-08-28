from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditToSlackBridgeHelper import fetch_latest_posts, send_posts_to_slack

router = APIRouter()

class RedditToSlackRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditToSlackBridge/0.1 by YourBot")
    subreddit_name: str
    limit: int = Field(default=3, description="Number of posts to forward")
    slack_webhook_url: str

@router.post("/reddit/bridge/slack")
def reddit_to_slack(request: RedditToSlackRequest):
    try:
        posts = fetch_latest_posts(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            subreddit_name=request.subreddit_name,
            limit=request.limit
        )

        result = send_posts_to_slack(
            slack_webhook_url=request.slack_webhook_url,
            posts=posts
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))