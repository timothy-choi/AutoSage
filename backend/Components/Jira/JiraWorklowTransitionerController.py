from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraWorkflowTransitionerHelper import transition_jira_issue

router = APIRouter()

class JiraWorkflowTransitionRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira base URL")
    email: str = Field(..., description="Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Issue key to transition (e.g., DEV-101)")
    target_status: str = Field(..., description="Target status to move the issue to (e.g., 'In Review')")

@router.post("/jira/transition-workflow")
def transition_issue(request: JiraWorkflowTransitionRequest):
    result = transition_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key,
        target_status=request.target_status
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result