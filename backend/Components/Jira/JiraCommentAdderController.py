from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraCommentAdderHelper import add_jira_comment

router = APIRouter()

class JiraCommentRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Key of the issue to comment on")
    comment_body: str = Field(..., description="Comment text")

@router.post("/jira/add-comment")
def add_comment(request: JiraCommentRequest):
    result = add_jira_comment(
        jira_base_url=request.jira_base_url,
        email=request.email,
        api_token=request.api_token,
        issue_key=request.issue_key,
        comment_body=request.comment_body
    )

    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["message"])

    return result