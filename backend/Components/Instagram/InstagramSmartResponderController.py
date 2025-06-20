from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from InstagramSmartResponderHelper import (
    generate_smart_reply,
    extract_intent,
    suggest_canned_response
)

router = APIRouter()

class SmartReplyRequest(BaseModel):
    message_text: str
    conversation_context: str = ""

class IntentRequest(BaseModel):
    message_text: str

class CannedResponseRequest(BaseModel):
    intent: str

@router.post("/instagram/smart-reply")
async def instagram_smart_reply(req: SmartReplyRequest):
    reply = await generate_smart_reply(req.message_text, req.conversation_context)
    if reply.startswith("Error"):
        raise HTTPException(status_code=500, detail=reply)
    return {"reply": reply}

@router.post("/instagram/intent")
async def instagram_extract_intent(req: IntentRequest):
    result = await extract_intent(req.message_text)
    return {"intent": result}

@router.post("/instagram/canned-response")
async def instagram_canned_response(req: CannedResponseRequest):
    response = await suggest_canned_response(req.intent)
    return {"response": response}