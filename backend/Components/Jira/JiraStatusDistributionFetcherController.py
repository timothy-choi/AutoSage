from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from JiraStatusDistributionFetcherHelper import get_jira_status_distribution

router = APIRouter()

class JiraStatusDistributionRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira base URL (e.g., https://company.atlassian.net)")
    email: EmailStr = Field(..., description="Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    project_key: str = Field(None, description="Jira project key (used if custom_jql is not provided)")
    custom_jql: str = Field(None, description="Optional JQL override (e.g., statusCategory != Done)")

@router.post("/jira/status-distribution")
def fetch_status_distribution(request: JiraStatusDistributionRequest):
    try:
        result = get_jira_status_distribution(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            project_key=request.project_key,
            custom_jql=request.custom_jql
        )
        return {"status_distribution": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))