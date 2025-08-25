from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime
from RedditPostSchedulerHelper import schedule_post

router = APIRouter()

class RedditPostScheduleRequest(BaseModel):
    client_id: str
    client_secret: str
    username: str
    password: str
    user_agent: str = Field(default="RedditPostScheduler/0.1 by YourBot")
    subreddit: str
    title: str
    body: str
    scheduled_time: datetime 

@router.post("/reddit/schedule_post")
def reddit_post_scheduler(request: RedditPostScheduleRequest):
    try:
        result = schedule_post(
            client_id=request.client_id,
            client_secret=request.client_secret,
            username=request.username,
            password=request.password,
            user_agent=request.user_agent,
            subreddit=request.subreddit,
            title=request.title,
            body=request.body,
            scheduled_time=request.scheduled_time
        )
        return {"status": "success", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))