from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List
from LinkedinMessageSenderHelper import (
    send_message_to_connection,
    batch_send_messages,
    check_connection_status,
    get_recent_conversations
)

router = APIRouter()

class MessagePayload(BaseModel):
    public_identifier: str
    message: str

class BatchMessagePayload(BaseModel):
    identifiers: List[str]
    message: str

@router.post("/linkedin/message")
def send_message(payload: MessagePayload):
    try:
        return send_message_to_connection(payload.public_identifier, payload.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/linkedin/messages")
def send_batch_messages(payload: BatchMessagePayload):
    try:
        return batch_send_messages(payload.identifiers, payload.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/linkedin/connection-status")
def get_connection_status(public_identifier: str = Query(...)):
    try:
        return check_connection_status(public_identifier)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/linkedin/conversations")
def list_recent_conversations(limit: int = Query(10, ge=1, le=100)):
    try:
        return get_recent_conversations(limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))