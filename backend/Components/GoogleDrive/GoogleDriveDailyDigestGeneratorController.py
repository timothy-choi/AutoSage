from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timedelta, timezone

from GoogleDriveDailyDigestGeneratorHelper import (
    fetch_recent_files, generate_digest_html, send_email_digest, send_slack_digest
)

router = APIRouter()

class DigestRequest(BaseModel):
    access_token: str = Field(..., description="OAuth2 token")
    smtp_host: Optional[str] = None
    smtp_port: Optional[int] = None
    smtp_user: Optional[str] = None
    smtp_password: Optional[str] = None
    from_email: Optional[str] = None
    to_email: Optional[str] = None
    slack_webhook_url: Optional[str] = None
    since_iso: Optional[str] = None  

@router.post("/gdrive/daily-digest")
def daily_digest(request: DigestRequest):
    try:
        since = request.since_iso or (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        files = fetch_recent_files(request.access_token, since)
        digest_html = generate_digest_html(files)

        result = {"status": "success", "file_count": len(files)}

        if request.to_email:
            email_res = send_email_digest(
                smtp_host=request.smtp_host,
                smtp_port=request.smtp_port,
                smtp_user=request.smtp_user,
                smtp_password=request.smtp_password,
                from_email=request.from_email,
                to_email=request.to_email,
                subject="Google Drive Daily Digest",
                html_content=digest_html
            )
            result["email"] = email_res

        if request.slack_webhook_url:
            slack_res = send_slack_digest(request.slack_webhook_url, digest_html)
            result["slack"] = slack_res

        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))