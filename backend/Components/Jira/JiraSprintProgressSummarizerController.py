from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraSprintProgressSummarizerHelper import summarize_jira_sprint_progress

router = APIRouter()

class JiraSprintProgressRequest(BaseModel):
    jira_base_url: str = Field(..., description="Jira instance URL")
    email: str = Field(..., description="Atlassian user email")
    api_token: str = Field(..., description="Jira API token")
    board_id: int = Field(..., description="Agile board ID")
    sprint_id: int = Field(..., description="Sprint ID")

@router.post("/jira/sprint-progress-summary")
def summarize_sprint_progress(request: JiraSprintProgressRequest):
    result = summarize_jira_sprint_progress(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        board_id=request.board_id,
        sprint_id=request.sprint_id
    )

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result