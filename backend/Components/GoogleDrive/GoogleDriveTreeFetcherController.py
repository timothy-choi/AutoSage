from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveTreeFetcherHelper import fetch_folder_tree

router = APIRouter()

class FolderTreeRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 access token")
    folder_id: str = Field(..., description="ID of the folder to start from")
    recursive: bool = Field(True, description="Whether to fetch folders recursively")

@router.post("/gdrive/folder-tree")
def get_folder_tree(request: FolderTreeRequest):
    try:
        return fetch_folder_tree(
            access_token=request.access_token,
            folder_id=request.folder_id,
            recursive=request.recursive
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))