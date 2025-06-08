from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from DiscordGPTResponderHelper import *

router = APIRouter()

class Msg(BaseModel):
    message: str

class MsgList(BaseModel):
    messages: List[str]

class LangRequest(BaseModel):
    message: str
    target_lang: str

@router.post("/discord/smart/gpt", response_model=Msg)
async def gpt_fallback(req: Msg):
    reply = await get_gpt_response(req.message)
    return Msg(message=reply)

@router.post("/discord/smart/summarize", response_model=Msg)
def summarize(req: MsgList):
    summary = summarize_conversation(req.messages)
    return Msg(message=summary)

@router.post("/discord/smart/mood", response_model=Msg)
def mood_reply(req: Msg):
    reply = respond_to_sentiment(req.message)
    return Msg(message=reply)

@router.post("/discord/smart/translate", response_model=Msg)
def translate(req: LangRequest):
    translated = auto_translate_response(req.message, req.target_lang)
    return Msg(message=translated)

@router.post("/discord/smart/topic", response_model=Msg)
def topic_detection(req: Msg):
    topic = detect_question_topic(req.message)
    return Msg(message=topic)