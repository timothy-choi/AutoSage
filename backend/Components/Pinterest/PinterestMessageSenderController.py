from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel
from PinterestMessageSenderHelper import send_message, list_conversations, list_messages

router = APIRouter(prefix="/pinterest/messages", tags=["Pinterest Message Sender"])

class MessageSendRequest(BaseModel):
    conversation_id: str
    text: str


@router.post("/")
def api_send_message(request: MessageSendRequest, authorization: str = Header(...)):
    try:
        return send_message(
            authorization.replace("Bearer ", ""),
            request.conversation_id,
            request.text
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/conversations")
def api_list_conversations(
    limit: int = Query(25, description="Max number of conversations to fetch"),
    authorization: str = Header(...)
):
    try:
        return list_conversations(authorization.replace("Bearer ", ""), limit)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{conversation_id}")
def api_list_messages(
    conversation_id: str,
    limit: int = Query(25, description="Max number of messages to fetch"),
    authorization: str = Header(...)
):
    try:
        return list_messages(
            authorization.replace("Bearer ", ""),
            conversation_id,
            limit
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))