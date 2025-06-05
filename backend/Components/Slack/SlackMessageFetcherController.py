from fastapi import APIRouter, Query, HTTPException
from SlackMessageFetcherHelper import fetch_slack_messages, fetch_thread_replies, fetch_user_messages, search_channel_messages

router = APIRouter()

@router.get("/slack/fetch-messages")
def get_slack_messages(
    token: str = Query(...),
    channel: str = Query(...),
    limit: int = Query(10)
):
    try:
        messages = fetch_slack_messages(token, channel, limit)
        return {"channel": channel, "messages": messages}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/slack/thread-replies")
def get_thread_replies(
    token: str = Query(...),
    channel: str = Query(...),
    thread_ts: str = Query(...)
):
    try:
        replies = fetch_thread_replies(token, channel, thread_ts)
        return {"thread_ts": thread_ts, "replies": replies}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/slack/user-messages")
def get_user_messages(
    token: str = Query(...),
    channel: str = Query(...),
    user_id: str = Query(...),
    limit: int = Query(20)
):
    try:
        user_msgs = fetch_user_messages(token, channel, user_id, limit)
        return {"user_id": user_id, "messages": user_msgs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/slack/search")
def search_messages(
    token: str = Query(...),
    channel: str = Query(...),
    keyword: str = Query(...),
    limit: int = Query(50)
):
    try:
        results = search_channel_messages(token, channel, keyword, limit)
        return {"matches": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))