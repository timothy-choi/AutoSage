from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveVersionTrackerHelper import (
    list_file_versions,
    delete_revision,
    keep_forever_revision
)

router = APIRouter()

class VersionTrackerRequest(BaseModel):
    access_token: str
    file_id: str
    max_results: int = 20

class VersionActionRequest(BaseModel):
    access_token: str
    file_id: str
    revision_id: str

class KeepForeverRequest(VersionActionRequest):
    keep: bool = True

@router.post("/gdrive/track-versions")
def track_versions(request: VersionTrackerRequest):
    try:
        return list_file_versions(
            access_token=request.access_token,
            file_id=request.file_id,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/gdrive/version")
def delete_version(request: VersionActionRequest):
    try:
        return delete_revision(
            access_token=request.access_token,
            file_id=request.file_id,
            revision_id=request.revision_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/gdrive/version/keep")
def toggle_keep_forever(request: KeepForeverRequest):
    try:
        return keep_forever_revision(
            access_token=request.access_token,
            file_id=request.file_id,
            revision_id=request.revision_id,
            keep=request.keep
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))