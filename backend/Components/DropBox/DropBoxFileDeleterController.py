from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Literal
from DropBoxFileDeleterHelper import (
    delete_file_from_dropbox,
    delete_multiple_files_from_dropbox,
    delete_if_older_than,
    soft_delete_file
)

router = APIRouter()

class SingleDeleteRequest(BaseModel):
    access_token: str
    path: str

class BatchDeleteRequest(BaseModel):
    access_token: str
    paths: List[str]

class ConditionalDeleteRequest(BaseModel):
    access_token: str
    path: str
    min_age_days: int

class SoftDeleteRequest(BaseModel):
    access_token: str
    path: str
    trash_folder: Optional[str] = "/Trash"

@router.post("/dropbox/delete")
def dropbox_delete(request: SingleDeleteRequest):
    try:
        return delete_file_from_dropbox(request.access_token, request.path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dropbox/delete-batch")
def dropbox_delete_batch(request: BatchDeleteRequest):
    try:
        return delete_multiple_files_from_dropbox(request.access_token, request.paths)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dropbox/delete-if-older")
def dropbox_delete_if_old(request: ConditionalDeleteRequest):
    try:
        return delete_if_older_than(
            access_token=request.access_token,
            path=request.path,
            min_age_days=request.min_age_days
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/dropbox/soft-delete")
def dropbox_soft_delete(request: SoftDeleteRequest):
    try:
        return soft_delete_file(
            access_token=request.access_token,
            path=request.path,
            trash_folder=request.trash_folder
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))