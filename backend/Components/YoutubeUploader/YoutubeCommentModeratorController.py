from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from YoutubeCommentModeratorHelper import moderate_and_optionally_delete

router = APIRouter()

class CommentModerationRequest(BaseModel):
    api_key: str = Field(..., description="YouTube Data API key")
    video_id: str = Field(..., description="YouTube video ID")
    banned_keywords: List[str] = Field(..., description="List of banned words or phrases")
    delete_flag: bool = Field(default=False, description="Whether to delete flagged comments")

@router.post("/youtube/moderate-comments")
def youtube_comment_moderator(request: CommentModerationRequest):
    try:
        result = moderate_and_optionally_delete(
            api_key=request.api_key,
            video_id=request.video_id,
            banned_keywords=request.banned_keywords,
            delete_flag=request.delete_flag
        )
        return {"flagged_comments": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))