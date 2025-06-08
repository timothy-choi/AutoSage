from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict
from DiscordSentimentAnalyzerHelper import analyze_sentiment

router = APIRouter()

class SentimentRequest(BaseModel):
    message: str

class SentimentResponse(BaseModel):
    sentiment: str
    compound: float
    details: Dict[str, float]

@router.post("/discord/sentiment/analyze", response_model=SentimentResponse)
async def analyze_discord_sentiment(req: SentimentRequest):
    result = analyze_sentiment(req.message)
    return SentimentResponse(
        sentiment=result["sentiment"],
        compound=result["compound"],
        details=result["details"]
    )