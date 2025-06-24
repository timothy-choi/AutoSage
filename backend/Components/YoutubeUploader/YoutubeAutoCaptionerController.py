from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from YoutubeAutoCaptionerHelper import auto_generate_youtube_caption

router = APIRouter()

class YouTubeCaptionRequest(BaseModel):
    url_or_id: str = Field(..., description="YouTube video URL or ID")

@router.post("/youtube/auto-caption")
def generate_youtube_caption(request: YouTubeCaptionRequest):
    result = auto_generate_youtube_caption(request.url_or_id)

    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result