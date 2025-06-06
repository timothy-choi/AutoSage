from fastapi import APIRouter, HTTPException, Query
from SmartSlackSummarizerHelper import fetch_and_summarize

router = APIRouter()

@router.get("/slack/summarize")
def summarize_slack_channel(
    token: str = Query(...),
    channel: str = Query(...),
    limit: int = Query(20)
):
    try:
        summary = fetch_and_summarize(token, channel, limit)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))