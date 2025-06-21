from fastapi import APIRouter, HTTPException
from FacebookPostInsightFetcherHelper import fetch_post_insights

router = APIRouter()

@router.get("/facebook/insights/post/{post_id}")
def get_post_insights(post_id: str):
    try:
        insights = fetch_post_insights(post_id)
        return {"post_id": post_id, "insights": insights}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))