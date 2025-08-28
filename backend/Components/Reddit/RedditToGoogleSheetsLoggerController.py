from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from RedditToGoogleSheetsLoggerHelper import RedditToGoogleSheetsLoggerHelper

router = APIRouter()

class LogRequest(BaseModel):
    reddit_token: str
    google_creds_json: Dict[str, Any] 
    sheet_name: str
    subreddit: str
    limit: int = 5

@router.post("/reddit-to-sheets/log")
def log_reddit_to_sheets(req: LogRequest):
    try:
        helper = RedditToGoogleSheetsLoggerHelper(
            req.reddit_token,
            req.google_creds_json,
            req.sheet_name
        )
        result = helper.log_subreddit_posts(req.subreddit, req.limit)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))