from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveFileMoverHelper import move_file_to_folder

router = APIRouter()

class FileMoveRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 token")
    file_id: str = Field(..., description="ID of the file to move")
    target_folder_id: str = Field(..., description="ID of the destination folder")

@router.post("/gdrive/move-file")
def move_file(request: FileMoveRequest):
    try:
        return move_file_to_folder(
            access_token=request.access_token,
            file_id=request.file_id,
            target_folder_id=request.target_folder_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))