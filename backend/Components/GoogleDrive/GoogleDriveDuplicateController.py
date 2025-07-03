from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveDuplicateFinderHelper import find_drive_duplicates

router = APIRouter()

class DuplicateFinderRequest(BaseModel):
    access_token: str = Field(..., description="OAuth token")
    strategy: str = Field("name", description="Duplicate detection strategy: name, name+size, name+size+type")
    max_results: int = Field(1000, description="Max number of files to check")

@router.post("/gdrive/find-duplicates")
def find_duplicates(request: DuplicateFinderRequest):
    try:
        return find_drive_duplicates(
            access_token=request.access_token,
            strategy=request.strategy,
            max_results=request.max_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))