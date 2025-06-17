from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramCaptionGeneratorHelper import generate_instagram_caption, generate_hashtags, generate_emojified_caption

router = APIRouter()

class CaptionRequest(BaseModel):
    prompt: str
    openai_api_key: str

class HashtagRequest(BaseModel):
    topic: str
    openai_api_key: str

@router.post("/instagram/generate-caption")
async def generate_caption(req: CaptionRequest):
    result = await generate_instagram_caption(req.prompt, req.openai_api_key)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/instagram/generate-hashtags")
async def generate_hashtags_api(req: HashtagRequest):
    result = await generate_hashtags(req.topic, req.openai_api_key)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result

@router.post("/instagram/generate-emojified-caption")
async def generate_emojified_caption_api(req: CaptionRequest):
    result = await generate_emojified_caption(req.prompt, req.openai_api_key)
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result