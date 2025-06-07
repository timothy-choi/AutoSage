from fastapi import APIRouter, Query, HTTPException
from DiscordThreadArchiverHelper import archive_inactive_threads

router = APIRouter()

@router.post("/discord/threads/archive")
def auto_archive_threads(
    token: str = Query(..., description="Discord bot token"),
    channel_id: str = Query(..., description="Parent channel ID"),
    inactive_minutes: int = Query(60, description="Minutes of inactivity before archiving")
):
    try:
        archived = archive_inactive_threads(token, channel_id, inactive_minutes)
        return {"archived_threads": archived}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))