import os
import requests
from typing import Optional, Dict

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWEET_URL = "https://api.twitter.com/2/tweets"

def reply_to_tweet(reply_text: str, in_reply_to_tweet_id: str, media_id: Optional[str] = None) -> Dict:
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "text": reply_text,
        "reply": {
            "in_reply_to_tweet_id": in_reply_to_tweet_id
        }
    }

    if media_id:
        payload["media"] = {"media_ids": [media_id]}

    res = requests.post(TWEET_URL, json=payload, headers=headers)
    if res.status_code in (200, 201):
        return res.json()
    raise Exception(f"Failed to reply to tweet: {res.status_code} - {res.text}")