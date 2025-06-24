from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeCommentReplierHelper import reply_to_youtube_comment

router = APIRouter()

class YouTubeCommentReplyRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token with YouTube comment access")
    parent_comment_id: str = Field(..., description="ID of the comment you want to reply to")
    reply_text: str = Field(..., description="The reply message text")

@router.post("/youtube/reply-to-comment")
def reply_to_comment(request: YouTubeCommentReplyRequest):
    result = reply_to_youtube_comment(
        access_token=request.access_token,
        parent_comment_id=request.parent_comment_id,
        reply_text=request.reply_text
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result