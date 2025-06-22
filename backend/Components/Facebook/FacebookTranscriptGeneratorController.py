from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from FacebookTranscriptGeneratorHelper import generate_transcript

router = APIRouter()

class PostModel(BaseModel):
    id: str
    message: str = ""
    created_time: str
    from_: Dict[str, str] = {}
    
    class Config:
        fields = {"from_": "from"}

class CommentModel(BaseModel):
    post_id: str
    message: str
    created_time: str
    from_: Dict[str, str] = {}

    class Config:
        fields = {"from_": "from"}

class TranscriptPayload(BaseModel):
    posts: List[PostModel]
    comments: List[CommentModel]

@router.post("/facebook/transcript/generate")
def create_transcript(payload: TranscriptPayload):
    try:
        posts = [post.dict(by_alias=True) for post in payload.posts]
        comments = [comment.dict(by_alias=True) for comment in payload.comments]
        result = generate_transcript(posts, comments)
        return {"transcript": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))