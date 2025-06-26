from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from JiraProjectMetricsCollectorHelper import collect_jira_project_metrics

router = APIRouter()

class JiraProjectMetricsRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: EmailStr = Field(..., description="Your Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    project_key: str = Field(..., description="Jira project key (e.g., DEV)")

@router.post("/jira/project-metrics")
def get_project_metrics(request: JiraProjectMetricsRequest):
    try:
        metrics = collect_jira_project_metrics(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            project_key=request.project_key
        )
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))