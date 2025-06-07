from fastapi import APIRouter, Query, HTTPException
from DiscordMessageModeratorHelper import fetch_recent_messages, scan_for_violations, delete_message

router = APIRouter()

@router.post("/discord/moderate/messages")
def moderate_channel_messages(
    token: str = Query(..., description="Bot token prefixed with 'Bot '"),
    channel_id: str = Query(..., description="Channel ID to moderate"),
    limit: int = Query(50, description="Number of recent messages to scan"),
    delete_flagged: bool = Query(False, description="Delete flagged messages automatically")
):
    try:
        messages = fetch_recent_messages(token, channel_id, limit)
        flagged = scan_for_violations(messages)

        report = []
        for msg, patterns in flagged:
            if delete_flagged:
                deleted = delete_message(token, channel_id, msg["id"])
            else:
                deleted = False

            report.append({
                "id": msg["id"],
                "author": msg["author"]["username"],
                "content": msg["content"],
                "matches": patterns,
                "deleted": deleted
            })

        return {"flagged_messages": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))