from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from NotionToGithubSyncerHelper import sync_notion_to_github

router = APIRouter()

class NotionGitHubSyncRequest(BaseModel):
    notion_token: str = Field(..., description="Notion API token")
    database_id: str = Field(..., description="Notion database ID")
    github_token: str = Field(..., description="GitHub personal access token")
    repo: str = Field(..., description="GitHub repository in 'owner/repo' format")
    max_items: int = Field(10, description="Number of Notion entries to sync")

@router.post("/notion/to-github")
def notion_to_github(request: NotionGitHubSyncRequest) -> List[Dict]:
    try:
        return sync_notion_to_github(
            notion_token=request.notion_token,
            database_id=request.database_id,
            github_token=request.github_token,
            repo=request.repo,
            max_items=request.max_items
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))