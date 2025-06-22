import os
import requests
from typing import Optional, Dict
from datetime import datetime

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

TWEET_URL = "https://api.twitter.com/2/tweets"

def post_tweet(text: str, media_id: Optional[str] = None) -> Dict:
    """
    Publish a tweet with optional media.
    """
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}
    if media_id:
        payload["media"] = {"media_ids": [media_id]}

    res = requests.post(TWEET_URL, json=payload, headers=headers)
    if res.status_code == 201 or res.status_code == 200:
        return res.json()
    raise Exception(f"Failed to post tweet: {res.status_code} - {res.text}")