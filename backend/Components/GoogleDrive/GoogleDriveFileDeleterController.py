from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Union

from GoogleDriveFileDeleterHelper import (
    delete_drive_file,
    trash_drive_file,
    get_file_metadata,
    batch_delete_files
)

router = APIRouter()

class SingleFileDeleteRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    file_id: str = Field(..., description="ID of the file to delete")
    permanent: bool = Field(True, description="If True, permanently delete. If False, move to trash.")
    preview: bool = Field(False, description="If True, return metadata and do not delete.")

class BatchFileDeleteRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    file_ids: List[str] = Field(..., description="List of file IDs to delete")
    permanent: bool = Field(True, description="Permanently delete or move to trash")

@router.post("/gdrive/delete-file")
def delete_file(request: SingleFileDeleteRequest):
    try:
        if request.preview:
            metadata = get_file_metadata(request.access_token, request.file_id)
            return {
                "status": "preview",
                "file_id": request.file_id,
                "metadata": metadata
            }

        if request.permanent:
            return delete_drive_file(request.access_token, request.file_id)
        else:
            return trash_drive_file(request.access_token, request.file_id)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/gdrive/delete-files")
def delete_files(request: BatchFileDeleteRequest):
    try:
        return batch_delete_files(
            access_token=request.access_token,
            file_ids=request.file_ids,
            permanent=request.permanent
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))