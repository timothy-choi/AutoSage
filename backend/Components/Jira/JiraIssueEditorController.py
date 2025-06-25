from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from JiraIssueEditorHelper import edit_jira_issue

router = APIRouter()

class JiraIssueEditRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL (e.g., https://yourdomain.atlassian.net)")
    email: str = Field(..., description="Your Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Issue key (e.g., DEV-123)")
    summary: Optional[str] = Field(None, description="New issue summary")
    description: Optional[str] = Field(None, description="New issue description")
    issue_type: Optional[str] = Field(None, description="New issue type")
    labels: Optional[List[str]] = Field(None, description="New list of labels")

@router.put("/jira/edit-issue")
def edit_issue(request: JiraIssueEditRequest):
    result = edit_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key,
        summary=request.summary,
        description=request.description,
        issue_type=request.issue_type,
        labels=request.labels
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result