from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraStatusUpdaterHelper import update_jira_status

router = APIRouter()

class JiraStatusUpdateRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira base URL")
    email: str = Field(..., description="Atlassian account email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Jira issue key (e.g., DEV-101)")
    target_status: str = Field(..., description="Desired target status (e.g., 'In Progress')")

@router.post("/jira/update-status")
def update_status(request: JiraStatusUpdateRequest):
    result = update_jira_status(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key,
        target_status=request.target_status
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result