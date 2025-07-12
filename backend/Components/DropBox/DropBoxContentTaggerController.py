from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from DropBoxContentTaggerHelper import tag_dropbox_file

router = APIRouter()

class DropboxTagRequest(BaseModel):
    access_token: str = Field(..., description="Dropbox API access token")
    path: str = Field(..., description="Path to the Dropbox file (e.g., /docs/meeting_notes.pdf)")

@router.post("/dropbox/content/tag")
def dropbox_content_tag(request: DropboxTagRequest):
    try:
        return tag_dropbox_file(request.access_token, request.path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))