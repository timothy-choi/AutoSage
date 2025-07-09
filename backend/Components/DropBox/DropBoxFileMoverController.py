from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from DropBoxFileMoverHelper import move_file_in_dropbox

router = APIRouter()

class DropboxMoveRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    from_path: str = Field(..., description="Source path in Dropbox (e.g., /docs/old.txt)")
    to_path: str = Field(..., description="Destination path in Dropbox (e.g., /archive/old.txt)")
    autorename: Optional[bool] = Field(False, description="Rename if destination exists")

@router.post("/dropbox/move")
def dropbox_move(request: DropboxMoveRequest):
    try:
        return move_file_in_dropbox(
            access_token=request.access_token,
            from_path=request.from_path,
            to_path=request.to_path,
            autorename=request.autorename
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))