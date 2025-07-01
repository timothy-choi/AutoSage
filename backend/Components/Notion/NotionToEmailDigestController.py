from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict
from NotionToEmailDigestHelper import run_notion_to_email_digest

router = APIRouter()

class SMTPInfo(BaseModel):
    host: str
    port: int
    username: str
    password: str

class EmailInfo(BaseModel):
    from_: str = Field(..., alias="from")
    to: str
    subject: str = "Your Notion Digest"

class NotionToEmailRequest(BaseModel):
    notion_token: str = Field(..., description="Integration token for Notion")
    database_id: str = Field(..., description="ID of the Notion database")
    smtp_info: SMTPInfo
    email_info: EmailInfo

@router.post("/notion/email-digest")
def notion_to_email_digest(request: NotionToEmailRequest):
    try:
        result = run_notion_to_email_digest(
            notion_token=request.notion_token,
            database_id=request.database_id,
            smtp_info=request.smtp_info.dict(),
            email_info=request.email_info.dict(by_alias=True)
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))