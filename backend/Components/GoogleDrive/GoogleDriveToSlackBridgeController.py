from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleDriveToSlackBridgeHelper import send_drive_files_to_slack

router = APIRouter()

class DriveFile(BaseModel):
    id: str
    name: Optional[str]
    size: Optional[str]
    mimeType: Optional[str]
    webViewLink: Optional[str]

class DriveToSlackRequest(BaseModel):
    slack_webhook_url: str = Field(..., description="Incoming Slack webhook URL")
    files: List[DriveFile] = Field(..., description="List of Drive files to forward")

@router.post("/gdrive/notify-slack")
def notify_slack(request: DriveToSlackRequest):
    try:
        return send_drive_files_to_slack(
            files=[file.dict() for file in request.files],
            slack_webhook_url=request.slack_webhook_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))