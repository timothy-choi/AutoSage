from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxToSlackBridgeHelper import notify_dropbox_file_to_slack

router = APIRouter()

class DropboxToSlackRequest(BaseModel):
    dropbox_access_token: str = Field(..., description="Dropbox access token")
    file_path: str = Field(..., description="Path to the Dropbox file (e.g., /docs/report.pdf)")
    file_name: str = Field(..., description="Name of the file (for display)")
    file_size: int = Field(..., description="Size of the file in bytes")
    slack_webhook_url: str = Field(..., description="Slack webhook URL")

@router.post("/dropbox/to/slack")
def dropbox_to_slack_bridge(request: DropboxToSlackRequest):
    try:
        return notify_dropbox_file_to_slack(
            dropbox_token=request.dropbox_access_token,
            file_path=request.file_path,
            file_name=request.file_name,
            file_size=request.file_size,
            slack_webhook=request.slack_webhook_url
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))