from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from RedditToDiscordBridgeHelper import fetch_latest_posts, send_posts_to_discord

router = APIRouter()

class RedditToDiscordRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditToDiscordBridge/0.1 by YourBot")
    subreddit_name: str
    limit: int = Field(default=3, description="Number of posts to forward")
    discord_webhook_url: str

@router.post("/reddit/bridge/discord")
def reddit_to_discord(request: RedditToDiscordRequest):
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

        result = send_posts_to_discord(
            discord_webhook_url=request.discord_webhook_url,
            posts=posts
        )

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))