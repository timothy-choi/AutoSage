from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from JiraSubtaskCreatorHelper import create_jira_subtask

router = APIRouter()

class JiraSubtaskRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Your Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    project_key: str = Field(..., description="Jira project key (e.g., DEV)")
    parent_issue_key: str = Field(..., description="Key of the parent issue (e.g., DEV-123)")
    summary: str = Field(..., description="Sub-task summary")
    description: Optional[str] = Field(default="", description="Optional sub-task description")
    subtask_type: Optional[str] = Field(default="Sub-task", description="Sub-task issue type")
    labels: Optional[List[str]] = Field(default_factory=list, description="Optional labels")

@router.post("/jira/create-subtask")
def create_subtask(request: JiraSubtaskRequest):
    result = create_jira_subtask(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        project_key=request.project_key,
        parent_issue_key=request.parent_issue_key,
        summary=request.summary,
        description=request.description,
        subtask_type=request.subtask_type,
        labels=request.labels
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result