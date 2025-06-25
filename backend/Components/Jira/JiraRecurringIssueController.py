from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraRecurringIssueHelper import create_recurring_jira_issue

router = APIRouter()

class JiraRecurringIssueRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira base URL")
    email: str = Field(..., description="Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    project_key: str = Field(..., description="Jira project key (e.g., DEV)")
    summary_template: str = Field(..., description="Summary with optional {{date}} placeholder")
    description_template: str = Field(default="", description="Optional description with {{date}}")
    issue_type: str = Field(default="Task", description="Jira issue type")

@router.post("/jira/schedule-recurring-issue")
def schedule_recurring_issue(request: JiraRecurringIssueRequest):
    result = create_recurring_jira_issue(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        project_key=request.project_key,
        summary_template=request.summary_template,
        description_template=request.description_template,
        issue_type=request.issue_type
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result