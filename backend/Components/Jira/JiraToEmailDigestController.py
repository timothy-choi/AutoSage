from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from JiraToEmailDigestHelper import fetch_jira_issues, build_email_digest, send_email_smtp

router = APIRouter()

class JiraToEmailDigestRequest(BaseModel):
    jira_base_url: str
    email: str
    api_token: str
    jql: str = Field(..., description="JQL query to select issues")
    recipients: list[EmailStr]
    smtp_server: str
    smtp_port: int
    smtp_username: str
    smtp_password: str
    from_email: EmailStr
    subject: str = "Jira Digest"

@router.post("/jira/email-digest")
def send_digest(request: JiraToEmailDigestRequest):
    try:
        issues = fetch_jira_issues(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            jql=request.jql
        )
        digest = build_email_digest(issues, request.jira_base_url)

        result = send_email_smtp(
            sender=request.from_email,
            recipient_list=request.recipients,
            subject=request.subject,
            html_content=digest,
            smtp_server=request.smtp_server,
            smtp_port=request.smtp_port,
            smtp_username=request.smtp_username,
            smtp_password=request.smtp_password
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))