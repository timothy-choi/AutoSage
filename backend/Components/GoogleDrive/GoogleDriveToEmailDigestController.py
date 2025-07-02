from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleDriveToEmailDigestHelper import send_drive_digest_email

router = APIRouter()

class DriveFile(BaseModel):
    id: str
    name: Optional[str]
    size: Optional[str]
    mimeType: Optional[str]
    webViewLink: Optional[str]

class EmailDigestRequest(BaseModel):
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str
    from_email: str
    to_email: str
    subject: str = Field("Google Drive File Digest")
    files: List[DriveFile]

@router.post("/gdrive/send-digest-email")
def send_digest_email(request: EmailDigestRequest):
    try:
        return send_drive_digest_email(
            smtp_host=request.smtp_host,
            smtp_port=request.smtp_port,
            smtp_user=request.smtp_user,
            smtp_password=request.smtp_password,
            from_email=request.from_email,
            to_email=request.to_email,
            subject=request.subject,
            files=[file.dict() for file in request.files]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))