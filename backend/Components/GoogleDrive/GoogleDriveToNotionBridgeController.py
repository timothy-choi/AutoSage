from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleDriveToNotionBridgeHelper import send_drive_files_to_notion

router = APIRouter()

class DriveFile(BaseModel):
    id: str
    name: Optional[str]
    size: Optional[str]
    mimeType: Optional[str]
    webViewLink: Optional[str]

class DriveToNotionRequest(BaseModel):
    notion_token: str = Field(..., description="Bearer token for Notion API")
    database_id: str = Field(..., description="Notion database ID")
    files: List[DriveFile] = Field(..., description="List of Google Drive files to record")

@router.post("/gdrive/notify-notion")
def send_to_notion(request: DriveToNotionRequest):
    try:
        return send_drive_files_to_notion(
            files=[file.dict() for file in request.files],
            notion_token=request.notion_token,
            database_id=request.database_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))