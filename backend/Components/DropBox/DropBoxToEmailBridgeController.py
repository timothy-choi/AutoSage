from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxToEmailBridgeHelper import generate_and_send_dropbox_digest

router = APIRouter()

class SMTPConfig(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    sender: str
    recipient: str

class DropboxEmailDigestRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox access token")
    folder_path: str = Field("/", description="Folder to check for uploads")
    hours: int = Field(24, description="How many past hours to look for uploads")
    send_email: bool = Field(False, description="Whether to actually send the email")
    smtp_config: Optional[SMTPConfig] = None

@router.post("/dropbox/email/digest")
def dropbox_email_digest(request: DropboxEmailDigestRequest):
    try:
        return generate_and_send_dropbox_digest(
            access_token=request.access_token,
            folder_path=request.folder_path,
            hours=request.hours,
            send_email=request.send_email,
            smtp_config=request.smtp_config.dict() if request.smtp_config else None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))