from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from GoogleDriveToJiraBridgeHelper import send_drive_files_to_jira

router = APIRouter()

class DriveFile(BaseModel):
    id: str
    name: Optional[str]
    size: Optional[str]
    mimeType: Optional[str]
    webViewLink: Optional[str]

class DriveToJiraRequest(BaseModel):
    jira_base_url: str = Field(..., description="Base URL of Jira instance")
    jira_email: str = Field(..., description="Your Jira account email")
    jira_api_token: str = Field(..., description="Jira API token")
    jira_project_key: str = Field(..., description="Jira project key to create issues in")
    files: List[DriveFile] = Field(..., description="List of Google Drive files")

@router.post("/gdrive/notify-jira")
def send_to_jira(request: DriveToJiraRequest):
    try:
        return send_drive_files_to_jira(
            files=[file.dict() for file in request.files],
            jira_base_url=request.jira_base_url,
            jira_email=request.jira_email,
            jira_api_token=request.jira_api_token,
            jira_project_key=request.jira_project_key
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))