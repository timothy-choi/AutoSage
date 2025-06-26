from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from JiraLabelFilterHelper import filter_issues_by_label

router = APIRouter()

class JiraLabelFilterRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: EmailStr = Field(..., description="Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    labels: list[str] = Field(..., description="List of labels to filter issues by")
    max_results: int = Field(10, description="Maximum number of issues to fetch")

@router.post("/jira/filter-by-label")
def filter_by_label(request: JiraLabelFilterRequest):
    try:
        issues = filter_issues_by_label(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            labels=request.labels,
            max_results=request.max_results
        )
        return {"issues": issues}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))