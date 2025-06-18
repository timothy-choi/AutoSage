from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from GoogleChatDailyDigestGeneratorHelper import (
    generate_googlechat_daily_digest,
    generate_digest_as_json,
    get_digest_summary_stats
)

router = APIRouter()

class DailyDigestEntry(BaseModel):
    sender: str
    content: str

class DailyDigestRequest(BaseModel):
    date: str
    messages: List[DailyDigestEntry]

@router.post("/googlechat/daily-digest")
async def googlechat_daily_digest(req: DailyDigestRequest, format: str = Query("txt", enum=["txt", "json"])):
    try:
        messages = [msg.dict() for msg in req.messages]
        if format == "json":
            path = await generate_digest_as_json(messages, req.date)
        else:
            path = await generate_googlechat_daily_digest(messages, req.date)
        return {"status": "success", "digest_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/googlechat/daily-digest/stats")
async def googlechat_digest_stats(req: DailyDigestRequest):
    try:
        messages = [msg.dict() for msg in req.messages]
        stats = await get_digest_summary_stats(messages)
        return {"status": "success", "summary_stats": stats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))