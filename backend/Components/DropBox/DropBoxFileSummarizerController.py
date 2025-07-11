from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxFileSummarizerHelper import summarize_dropbox_file

router = APIRouter()

class DropboxSummarizeRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path to the file in Dropbox (e.g. /notes/todo.txt)")

@router.post("/dropbox/summarize")
def dropbox_file_summarize(request: DropboxSummarizeRequest):
    try:
        return summarize_dropbox_file(
            access_token=request.access_token,
            path=request.path
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))