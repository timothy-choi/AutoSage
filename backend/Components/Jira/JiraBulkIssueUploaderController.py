from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from JiraBulkIssueUploaderHelper import bulk_upload_issues

router = APIRouter()

class JiraIssueItem(BaseModel):
    summary: str
    description: Optional[str] = ""
    issue_type: Optional[str] = "Task"
    assignee: Optional[str] = None

class JiraBulkUploadRequest(BaseModel):
    jira_base_url: str
    email: EmailStr
    api_token: str
    project_key: str
    issues: List[JiraIssueItem]

@router.post("/jira/bulk-upload")
def upload_bulk_issues(request: JiraBulkUploadRequest):
    try:
        result = bulk_upload_issues(
            jira_base_url=request.jira_base_url,
            email=request.email,
            api_token=request.api_token,
            project_key=request.project_key,
            issues=[issue.dict() for issue in request.issues]
        )
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))