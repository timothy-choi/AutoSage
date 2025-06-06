import requests
from textblob import TextBlob
from typing import List, Dict

def fetch_slack_messages(token: str, channel: str, limit: int = 20) -> List[str]:
    headers = {"Authorization": f"Bearer {token}"}
    params = {"channel": channel, "limit": limit}
    response = requests.get("https://slack.com/api/conversations.history", headers=headers, params=params)
    response_data = response.json()

    if not response_data.get("ok"):
        raise Exception(response_data.get("error", "Failed to fetch messages"))

    return [msg.get("text", "") for msg in response_data.get("messages", []) if "text" in msg]

def analyze_sentiment(text: str) -> Dict:
    blob = TextBlob(text)
    return {
        "polarity": blob.sentiment.polarity,     
        "subjectivity": blob.sentiment.subjectivity 
    }

def analyze_messages_sentiment(messages: List[str]) -> Dict:
    results = [analyze_sentiment(msg) for msg in messages]
    avg_polarity = sum(r["polarity"] for r in results) / len(results) if results else 0
    avg_subjectivity = sum(r["subjectivity"] for r in results) / len(results) if results else 0

    return {
        "average_polarity": avg_polarity,
        "average_subjectivity": avg_subjectivity,
        "individual_results": results
    }

def fetch_and_analyze_sentiment(token: str, channel: str, limit: int = 20) -> Dict:
    messages = fetch_slack_messages(token, channel, limit)
    return analyze_messages_sentiment(messages)