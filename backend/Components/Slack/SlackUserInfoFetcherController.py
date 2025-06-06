from fastapi import APIRouter, HTTPException, Query
from SlackUserInfoFetcherController import fetch_slack_user_info

router = APIRouter()

@router.get("/slack/user-info")
def get_user_info(token: str = Query(...), user_id: str = Query(...)):
    """
    Fetch basic Slack user information.
    """
    try:
        info = fetch_slack_user_info(token, user_id)
        return {"user_info": info}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))