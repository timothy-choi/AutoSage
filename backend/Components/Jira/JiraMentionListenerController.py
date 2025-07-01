from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraMentionListenerHelper import search_jira_mentions

router = APIRouter()

class JiraMentionRequest(BaseModel):
    jira_domain: str = Field(..., description="Your Jira domain (e.g., yourcompany.atlassian.net)")
    jira_email: str = Field(..., description="Email for Jira API auth")
    jira_token: str = Field(..., description="Jira API token")
    username_or_account_id: str = Field(..., description="The @username or accountId to search for")
    max_results: int = Field(default=10, description="Max number of issues to search")

@router.post("/jira/mentions")
def jira_mentions(request: JiraMentionRequest):
    try:
        results = search_jira_mentions(
            jira_domain=request.jira_domain,
            jira_email=request.jira_email,
            jira_token=request.jira_token,
            username_or_account_id=request.username_or_account_id,
            max_results=request.max_results
        )
        return {"mentions": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))