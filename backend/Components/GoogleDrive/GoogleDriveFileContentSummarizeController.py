from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from GoogleDriveFileContentSummarizerHelper import summarize_drive_file

router = APIRouter()

class FileSummaryRequest(BaseModel):
    access_token: str = Field(..., description="OAuth 2.0 token with Drive access")
    file_id: str = Field(..., description="ID of the file to summarize")
    mime_type: str = Field(..., description="MIME type of the file")
    max_sentences: int = Field(3, description="Number of sentences in summary")

@router.post("/gdrive/summarize-file")
def summarize_file(request: FileSummaryRequest):
    try:
        return summarize_drive_file(
            access_token=request.access_token,
            file_id=request.file_id,
            mime_type=request.mime_type,
            max_sentences=request.max_sentences
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))