from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraIssueDeleterHelper import delete_jira_issue

router = APIRouter()

class JiraIssueDeleteRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Issue key to delete")

@router.delete("/jira/delete-issue")
def delete_issue(request: JiraIssueDeleteRequest):
    result = delete_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result