from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from JiraIssueSearcherHelper import search_jira_issues

router = APIRouter()

class JiraIssueSearchRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Your Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    jql: str = Field(..., description="Jira Query Language string")
    max_results: Optional[int] = Field(default=10, description="Number of issues to return")

@router.post("/jira/search-issues")
def search_issues(request: JiraIssueSearchRequest):
    result = search_jira_issues(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        jql=request.jql,
        max_results=request.max_results
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result