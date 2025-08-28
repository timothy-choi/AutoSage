from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from RedditToNotionSyncerHelper import RedditToNotionSyncerHelper

router = APIRouter()

class SyncRequest(BaseModel):
    reddit_token: str
    notion_token: str
    notion_db_id: str
    subreddit: str
    limit: int = 5

@router.post("/reddit-to-notion/sync")
def sync_reddit_to_notion(req: SyncRequest):
    try:
        helper = RedditToNotionSyncerHelper(req.reddit_token, req.notion_token, req.notion_db_id)
        result = helper.sync_subreddit_posts(req.subreddit, req.limit)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))