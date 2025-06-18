from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from GoogleChatTranscriptGeneratorHelper import (
    generate_googlechat_transcript,
    generate_transcript_as_json,
    generate_transcript_as_csv
)

router = APIRouter()

class MessageEntry(BaseModel):
    timestamp: str
    sender: str
    content: str

class TranscriptRequest(BaseModel):
    thread_id: str
    messages: List[MessageEntry]

@router.post("/googlechat/generate-transcript")
async def googlechat_generate_transcript(req: TranscriptRequest, format: str = Query("txt", enum=["txt", "json", "csv"])):
    try:
        messages = [msg.dict() for msg in req.messages]
        if format == "json":
            path = await generate_transcript_as_json(messages, req.thread_id)
        elif format == "csv":
            path = await generate_transcript_as_csv(messages, req.thread_id)
        else:
            path = await generate_googlechat_transcript(messages, req.thread_id)

        return {"status": "success", "transcript_path": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
