from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
from NotionToJiraBridgeHelper import sync_notion_to_jira

router = APIRouter()

class NotionToJiraRequest(BaseModel):
    notion_token: str = Field(..., description="Notion integration token")
    database_id: str = Field(..., description="Notion database ID")
    jira_email: str = Field(..., description="Your Jira account email")
    jira_token: str = Field(..., description="Jira API token")
    jira_base_url: str = Field(..., description="Base URL of Jira (e.g. https://yourdomain.atlassian.net)")
    project_key: str = Field(..., description="Key of the target Jira project (e.g. 'ABC')")
    max_items: int = Field(10, description="Max Notion items to sync")

@router.post("/notion/to-jira")
def notion_to_jira_bridge(request: NotionToJiraRequest) -> List[Dict]:
    try:
        return sync_notion_to_jira(
            notion_token=request.notion_token,
            database_id=request.database_id,
            jira_email=request.jira_email,
            jira_token=request.jira_token,
            jira_base_url=request.jira_base_url,
            project_key=request.project_key,
            max_items=request.max_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))