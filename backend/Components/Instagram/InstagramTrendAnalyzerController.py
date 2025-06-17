from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from InstagramTrendAnalyzerHelper import analyze_trending_hashtags, compare_hashtag_trends

router = APIRouter()

class TrendRequest(BaseModel):
    user_id: str
    access_token: str
    hashtags: List[str]

@router.post("/instagram/trend-analysis")
async def trend_analysis(req: TrendRequest):
    result = await analyze_trending_hashtags(req.user_id, req.access_token, req.hashtags)
    if not result["trend_data"]:
        raise HTTPException(status_code=404, detail="No trend data found.")
    return result

@router.post("/instagram/compare-trend-data")
async def compare_trends(req: TrendRequest):
    trend_result = await analyze_trending_hashtags(req.user_id, req.access_token, req.hashtags)
    comparison = await compare_hashtag_trends(trend_result["trend_data"])
    return comparison