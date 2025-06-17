from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramEngagementAnalyzerHelper import get_engagement_data

router = APIRouter()

class EngagementRequest(BaseModel):
    instagram_account_id: str
    access_token: str

@router.post("/instagram/engagement-data")
async def engagement_data(req: EngagementRequest):
    result = await get_engagement_data(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result