from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict
from TeamsDailyDigestGeneratorHelper import (
    send_teams_digest,
    send_digest_with_links,
    send_conditional_digest
)

router = APIRouter()

class DigestRequest(BaseModel):
    webhook_url: str
    title: str
    summary_points: List[str]

class DigestLinksRequest(BaseModel):
    webhook_url: str
    title: str
    summary_links: List[Dict[str, str]]  # Each dict has 'text' and 'url'

class DigestConditionalRequest(BaseModel):
    webhook_url: str
    title: str
    data: Dict[str, str]
    include_keys: List[str]

@router.post("/teams/send-daily-digest")
async def send_daily_digest(req: DigestRequest):
    result = await send_teams_digest(req.webhook_url, req.title, req.summary_points)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-digest-with-links")
async def send_digest_links(req: DigestLinksRequest):
    result = await send_digest_with_links(req.webhook_url, req.title, req.summary_links)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result

@router.post("/teams/send-conditional-digest")
async def send_conditional(req: DigestConditionalRequest):
    result = await send_conditional_digest(req.webhook_url, req.title, req.data, req.include_keys)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result