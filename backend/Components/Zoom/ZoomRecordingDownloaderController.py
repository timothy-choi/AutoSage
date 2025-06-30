from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from ZoomRecordingDownloaderHelper import (
    fetch_meeting_recordings,
    download_recordings
)

router = APIRouter()

class ZoomRecordingDownloadRequest(BaseModel):
    meeting_id: str = Field(..., description="Zoom meeting ID")
    jwt_token: str = Field(..., description="Zoom JWT token")
    download_files: bool = Field(default=True, description="Whether to download files or just return links")
    save_dir: Optional[str] = Field(default="./zoom_recordings", description="Where to save downloaded files")

@router.post("/zoom/download-recordings")
def zoom_download_recordings(request: ZoomRecordingDownloadRequest):
    try:
        recordings = fetch_meeting_recordings(request.meeting_id, request.jwt_token)

        if not recordings:
            return {"message": "No recordings found."}

        if request.download_files:
            result = download_recordings(recordings, request.jwt_token, request.save_dir)
        else:
            result = [{"download_url": r["download_url"], "file_type": r.get("file_type")} for r in recordings]

        return {"recordings": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))