from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from TeamsMediaSummarizerHelper import download_image, summarize_image_text
import os

router = APIRouter()

class MediaSummaryRequest(BaseModel):
    file_url: str
    access_token: str

@router.post("/teams/summarize-image")
async def summarize_teams_image(req: MediaSummaryRequest):
    try:
        image_path = await download_image(req.file_url, req.access_token)
        summary = summarize_image_text(image_path)
        os.remove(image_path)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))