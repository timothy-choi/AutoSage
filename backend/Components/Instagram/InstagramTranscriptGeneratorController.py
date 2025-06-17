from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramTranscriptGeneratorHelper import get_video_url, generate_transcript_from_video

router = APIRouter()

class TranscriptRequest(BaseModel):
    media_id: str
    access_token: str
    whisper_api_key: str

@router.post("/instagram/generate-transcript")
async def generate_transcript(req: TranscriptRequest):
    media_url = await get_video_url(req.media_id, req.access_token)
    if not media_url:
        raise HTTPException(status_code=404, detail="Video media not found or unsupported type.")

    transcript = await generate_transcript_from_video(media_url, req.whisper_api_key)
    if "error" in transcript:
        raise HTTPException(status_code=500, detail=transcript)
    return transcript