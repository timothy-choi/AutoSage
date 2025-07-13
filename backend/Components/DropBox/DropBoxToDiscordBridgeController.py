from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxToDiscordBridgeHelper import notify_dropbox_file_to_discord

router = APIRouter()

class DropboxToDiscordRequest(BaseModel):
    dropbox_access_token: str = Field(..., description="Dropbox API access token")
    file_path: str = Field(..., description="Path of Dropbox file (e.g., /docs/report.pdf)")
    file_name: str = Field(..., description="Name of the file")
    file_size: int = Field(..., description="Size of the file in bytes")
    discord_webhook_url: str = Field(..., description="Discord webhook URL for the target channel")

@router.post("/dropbox/to/discord")
def dropbox_to_discord_bridge(request: DropboxToDiscordRequest):
    try:
        return notify_dropbox_file_to_discord(
            dropbox_token=request.dropbox_access_token,
            file_path=request.file_path,
            file_name=request.file_name,
            file_size=request.file_size,
            discord_webhook_url=request.discord_webhook_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))