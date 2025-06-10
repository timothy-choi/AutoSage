from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
from TeamsTranscriptGeneratorHelper import download_audio_file, generate_transcript

router = APIRouter()

class TranscriptRequest(BaseModel):
    file_url: str
    access_token: str

@router.post("/teams/generate-transcript")
async def teams_transcript_api(req: TranscriptRequest):
    try:
        audio_path = await download_audio_file(req.file_url, req.access_token)
        transcript = generate_transcript(audio_path)
        os.remove(audio_path)
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))