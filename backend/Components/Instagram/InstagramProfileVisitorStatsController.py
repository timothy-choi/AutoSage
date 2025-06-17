from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramProfileVisitorStatsHelper import get_profile_visits, get_profile_reach, get_profile_impressions

router = APIRouter()

class ProfileStatsRequest(BaseModel):
    instagram_account_id: str
    access_token: str

@router.post("/instagram/profile-visits")
async def profile_visits(req: ProfileStatsRequest):
    result = await get_profile_visits(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/profile-reach")
async def profile_reach(req: ProfileStatsRequest):
    result = await get_profile_reach(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/profile-impressions")
async def profile_impressions(req: ProfileStatsRequest):
    result = await get_profile_impressions(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result