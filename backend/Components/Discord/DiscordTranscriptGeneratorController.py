from fastapi import APIRouter, Query, HTTPException
from DiscordTranscriptGeneratorHelper import fetch_channel_messages, format_transcript, save_transcript_to_file

router = APIRouter()

@router.get("/discord/transcript")
def get_channel_transcript(
    token: str = Query(..., description="Bot token (prefixed with 'Bot ')"),
    channel_id: str = Query(..., description="Channel ID to fetch messages from"),
    limit: int = Query(50, description="Number of messages to include in transcript"),
    format_type: str = Query("text", description="Format: 'text' or 'json'"),
    save: bool = Query(False, description="Whether to save to file")
):
    try:
        messages = fetch_channel_messages(token, channel_id, limit)
        transcript = format_transcript(messages, format_type)

        if save:
            path = save_transcript_to_file(transcript, f"transcript_{channel_id}.{format_type}")
            return {"message": "Transcript saved", "path": path}

        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))