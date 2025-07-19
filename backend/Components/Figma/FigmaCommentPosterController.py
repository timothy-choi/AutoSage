from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from FigmaCommentPosterHelper import post_figma_comment

router = APIRouter()

class FigmaCommentRequest(BaseModel):
    file_key: str
    access_token: str
    message: str
    client_meta: Dict[str, float] 

@router.post("/figma/post-comment")
def post_comment(request: FigmaCommentRequest):
    return post_figma_comment(
        file_key=request.file_key,
        access_token=request.access_token,
        message=request.message,
        client_meta=request.client_meta
    )