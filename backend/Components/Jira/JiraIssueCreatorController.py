from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from JiraIssueCreatorHelper import create_jira_issue

router = APIRouter()

class JiraIssueRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your JIRA base URL (e.g., https://yourdomain.atlassian.net)")
    email: str = Field(..., description="Your Atlassian email")
    api_token: str = Field(..., description="JIRA API token")
    project_key: str = Field(..., description="Project key (e.g., DEV)")
    summary: str = Field(..., description="Short issue title")
    description: str = Field(..., description="Detailed description")
    issue_type: str = Field(default="Task", description="Type: Task, Bug, Story, etc.")
    labels: Optional[List[str]] = Field(default_factory=list)

@router.post("/jira/create-issue")
def create_issue(request: JiraIssueRequest):
    result = create_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        project_key=request.project_key,
        summary=request.summary,
        description=request.description,
        issue_type=request.issue_type,
        labels=request.labels
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result