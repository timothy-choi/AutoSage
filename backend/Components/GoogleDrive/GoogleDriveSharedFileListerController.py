from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List
from GoogleDriveSharedFileListerHelper import list_files_shared_by_me, list_shared_with_me_files, sort_files, files_to_csv

router = APIRouter()

class SharedFileListRequest(BaseModel):
    access_token: str
    max_results: int = 20
    list_type: str = Field("shared_with_me", description="shared_with_me or shared_by_me")
    sort_by: str = Field("name", description="field to sort by")
    order: str = Field("asc", description="asc or desc")
    as_csv: bool = False

@router.post("/gdrive/list-shared")
def list_shared(request: SharedFileListRequest):
    try:
        if request.list_type == "shared_with_me":
            files = list_shared_with_me_files(request.access_token, request.max_results)
        elif request.list_type == "shared_by_me":
            files = list_files_shared_by_me(request.access_token, request.max_results)
        else:
            raise HTTPException(status_code=400, detail="Invalid list_type")

        files = sort_files(files, request.sort_by, request.order)

        if request.as_csv:
            return {"csv": files_to_csv(files)}
        return files

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
