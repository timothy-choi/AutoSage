from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraToGithubBridgeHelper import sync_jira_to_github

router = APIRouter()

class JiraToGitHubRequest(BaseModel):
    jira_base_url: str = Field(..., description="Your Jira base URL")
    email: str = Field(..., description="Jira/Atlassian email")
    api_token: str = Field(..., description="Jira API token")
    issue_key: str = Field(..., description="Key of the Jira issue (e.g., DEV-42)")
    github_owner: str = Field(..., description="GitHub username or organization")
    github_repo: str = Field(..., description="GitHub repository name")
    github_token: str = Field(..., description="GitHub personal access token")

@router.post("/jira/to-github")
def jira_to_github(request: JiraToGitHubRequest):
    try:
        result = sync_jira_to_github(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            issue_key=request.issue_key,
            github_owner=request.github_owner,
            github_repo=request.github_repo,
            github_token=request.github_token
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))