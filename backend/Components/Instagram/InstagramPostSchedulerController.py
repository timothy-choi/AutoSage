from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramPostSchedulerHelper import schedule_instagram_post

router = APIRouter()

class PostScheduleRequest(BaseModel):
    image_url: str
    caption: str
    post_time: str  
    access_token: str
    instagram_account_id: str

@router.post("/instagram/schedule-post")
async def schedule_post(req: PostScheduleRequest):
    try:
        result = await schedule_instagram_post(
            req.image_url,
            req.caption,
            req.post_time,
            req.access_token,
            req.instagram_account_id
        )
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))