from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
from FigmaAutoCommentGeneratorHelper import generate_auto_comment

router = APIRouter()

class FigmaAutoCommentRequest(BaseModel):
    file_key: str
    access_token: str
    comment: str
    position: Dict[str, float]  
    client_meta: Optional[Dict[str, float]] = None  

@router.post("/figma/auto-comment")
def post_auto_comment(request: FigmaAutoCommentRequest):
    return generate_auto_comment(
        file_key=request.file_key,
        access_token=request.access_token,
        comment=request.comment,
        position=request.position,
        client_meta=request.client_meta
    )