from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from JiraToNotionBridgeHelper import sync_jira_to_notion

router = APIRouter()

class JiraToNotionRequest(BaseModel):
    jira_domain: str = Field(..., description="Your Jira domain (e.g., yourcompany.atlassian.net)")
    project_key: str = Field(..., description="Jira project key")
    jira_email: str = Field(..., description="Email for Jira authentication")
    jira_token: str = Field(..., description="Jira API token")
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Notion database ID")
    max_results: int = Field(default=5, description="Number of Jira issues to fetch")

@router.post("/jira/sync-to-notion")
def jira_to_notion_bridge(request: JiraToNotionRequest):
    try:
        result = sync_jira_to_notion(
            jira_domain=request.jira_domain,
            project_key=request.project_key,
            jira_email=request.jira_email,
            jira_token=request.jira_token,
            notion_token=request.notion_token,
            database_id=request.database_id,
            max_results=request.max_results
        )
        return {"synced": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))