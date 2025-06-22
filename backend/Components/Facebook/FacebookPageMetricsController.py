from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from FacebookPageMetricsHelper import fetch_page_insights

router = APIRouter()

class MetricsPayload(BaseModel):
    page_id: str
    metrics: List[str] = [
        "page_impressions",
        "page_engaged_users",
        "page_views_total",
        "page_fan_adds",
        "page_fans"
    ]

@router.post("/facebook/page/metrics")
def collect_page_metrics(payload: MetricsPayload):
    try:
        results = fetch_page_insights(payload.page_id, payload.metrics)
        return {"metrics": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))