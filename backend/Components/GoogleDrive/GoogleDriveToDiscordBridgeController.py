from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleDriveToDiscordBridgeHelper import send_drive_files_to_discord

router = APIRouter()

class DriveFile(BaseModel):
    id: str
    name: Optional[str]
    size: Optional[str]
    mimeType: Optional[str]
    webViewLink: Optional[str]

class DriveToDiscordRequest(BaseModel):
    discord_webhook_url: str = Field(..., description="Discord webhook URL")
    files: List[DriveFile] = Field(..., description="List of Google Drive files to notify")

@router.post("/gdrive/notify-discord")
def send_to_discord(request: DriveToDiscordRequest):
    try:
        return send_drive_files_to_discord(
            files=[file.dict() for file in request.files],
            discord_webhook_url=request.discord_webhook_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))