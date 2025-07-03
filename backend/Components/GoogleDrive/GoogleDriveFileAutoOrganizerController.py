from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveFileAutoOrganizerHelper import auto_organize_files

router = APIRouter()

class AutoOrganizerRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    strategy: str = Field("type", description="Organize by: type, size")
    max_results: int = Field(50, description="Max number of files to process")

@router.post("/gdrive/auto-organize")
def auto_organize(request: AutoOrganizerRequest):
    try:
        return auto_organize_files(
            access_token=request.access_token,
            strategy=request.strategy,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))