from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxToNotionBridgeHelper import bridge_dropbox_to_notion

router = APIRouter()

class DropboxToNotionRequest(BaseModel):
    dropbox_access_token: str = Field(..., description="Dropbox API access token")
    notion_access_token: str = Field(..., description="Notion API integration token")
    notion_database_id: str = Field(..., description="Notion database ID where pages will be created")
    folder_path: Optional[str] = Field("", description="Dropbox folder path to scan for files")
    max_files: Optional[int] = Field(20, description="Max number of files to process")

@router.post("/dropbox/to/notion")
def dropbox_to_notion_bridge(request: DropboxToNotionRequest):
    try:
        return bridge_dropbox_to_notion(
            dropbox_token=request.dropbox_access_token,
            notion_token=request.notion_access_token,
            notion_database_id=request.notion_database_id,
            folder_path=request.folder_path,
            max_files=request.max_files
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))