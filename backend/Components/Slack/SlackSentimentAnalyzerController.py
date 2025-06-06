from fastapi import APIRouter, Query, HTTPException
from SlackSentimentAnalyzerHelper import fetch_and_analyze_sentiment

router = APIRouter()

@router.get("/slack/sentiment")
def get_sentiment_analysis(
    token: str = Query(..., description="Slack Bot token"),
    channel: str = Query(..., description="Slack channel ID"),
    limit: int = Query(20, description="Number of messages to analyze")
):
    try:
        result = fetch_and_analyze_sentiment(token, channel, limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))