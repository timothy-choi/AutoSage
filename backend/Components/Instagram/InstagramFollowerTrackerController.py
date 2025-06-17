from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramFollowerTrackerHelper import get_follower_count, get_follower_metric_snapshot, compare_follower_counts

router = APIRouter()

class FollowerRequest(BaseModel):
    instagram_account_id: str
    access_token: str

class FollowerCompareRequest(BaseModel):
    before_count: int
    after_count: int

@router.post("/instagram/follower-count")
async def follower_count(req: FollowerRequest):
    result = await get_follower_count(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/follower-snapshot")
async def follower_snapshot(req: FollowerRequest):
    result = await get_follower_metric_snapshot(req.instagram_account_id, req.access_token)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result)
    return result

@router.post("/instagram/follower-compare")
async def follower_compare(req: FollowerCompareRequest):
    return await compare_follower_counts(req.before_count, req.after_count)