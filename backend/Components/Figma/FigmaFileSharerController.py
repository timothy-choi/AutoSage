from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from FigmaFileSharerHelper import share_figma_file

router = APIRouter()

class FigmaFileShareRequest(BaseModel):
    file_key: str
    access_token: str
    emails: List[str]
    role: str = "viewer" 

@router.post("/figma/share-file")
def share_file(request: FigmaFileShareRequest):
    return share_figma_file(
        file_key=request.file_key,
        access_token=request.access_token,
        emails=request.emails,
        role=request.role
    )