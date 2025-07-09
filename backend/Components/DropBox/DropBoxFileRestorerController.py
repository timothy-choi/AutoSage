from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxFileRestorerHelper import restore_file_to_revision, list_file_revisions

router = APIRouter()

class RestoreRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path to file in Dropbox")
    rev: str = Field(..., description="Revision ID to restore to")

class RevisionListRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path to file in Dropbox")
    limit: Optional[int] = Field(10, description="Number of revisions to list")

@router.post("/dropbox/restore")
def dropbox_restore(request: RestoreRequest):
    try:
        return restore_file_to_revision(
            access_token=request.access_token,
            path=request.path,
            rev=request.rev
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dropbox/revisions")
def dropbox_list_revisions(request: RevisionListRequest):
    try:
        return list_file_revisions(
            access_token=request.access_token,
            path=request.path,
            limit=request.limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))