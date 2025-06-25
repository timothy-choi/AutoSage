from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from JiraAutoCloserHelper import auto_close_jira_issue

router = APIRouter()

class JiraAutoCloseRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Issue key to close")
    done_keywords: Optional[List[str]] = Field(
        default=["done", "closed", "resolved"],
        description="List of acceptable terminal states to match against"
    )

@router.post("/jira/auto-close")
def auto_close(request: JiraAutoCloseRequest):
    result = auto_close_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key,
        done_keywords=[s.lower() for s in request.done_keywords]
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result