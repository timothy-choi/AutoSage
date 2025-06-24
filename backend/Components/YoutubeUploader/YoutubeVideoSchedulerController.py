from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from YoutubeVideoSchedulerHelper import schedule_youtube_upload

router = APIRouter()

class YouTubeVideoScheduleRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 access token for YouTube API")
    video_path: str = Field(..., description="Path to video file")
    title: str = Field(..., description="Video title")
    description: str = Field(..., description="Video description")
    scheduled_time: int = Field(..., description="UNIX timestamp for scheduled upload")
    privacy_status: str = Field(default="private", description="public | unlisted | private")
    tags: Optional[List[str]] = Field(default_factory=list)

@router.post("/youtube/schedule-upload")
def schedule_video_upload(request: YouTubeVideoScheduleRequest, background_tasks: BackgroundTasks):
    now = int(datetime.utcnow().timestamp())
    if request.scheduled_time <= now:
        raise HTTPException(status_code=400, detail="Scheduled time must be in the future.")

    background_tasks.add_task(
        schedule_youtube_upload,
        access_token=request.access_token,
        video_path=request.video_path,
        title=request.title,
        description=request.description,
        scheduled_unix_time=request.scheduled_time,
        privacy_status=request.privacy_status,
        tags=request.tags
    )

    return {
        "status": "scheduled",
        "message": f"Video will be uploaded at {datetime.utcfromtimestamp(request.scheduled_time)} UTC"
    }