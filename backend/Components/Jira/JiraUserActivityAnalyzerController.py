from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from JiraUserActivityAnalyzerHelper import analyze_jira_user_activity

router = APIRouter()

class JiraUserActivityRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira instance URL")
    email: str = Field(..., description="Atlassian auth email")
    api_token: str = Field(..., description="API token")
    user_email: str = Field(..., description="Email of the user to analyze")
    days: Optional[int] = Field(default=7, description="Days to look back")

@router.post("/jira/user-activity")
def get_user_activity(request: JiraUserActivityRequest):
    try:
        result = analyze_jira_user_activity(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            user_email=request.user_email,
            days=request.days
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))