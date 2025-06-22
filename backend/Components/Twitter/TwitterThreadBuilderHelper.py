import os
import requests
from typing import List, Optional, Dict

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
TWEET_URL = "https://api.twitter.com/2/tweets"

def post_tweet(text: str, in_reply_to_tweet_id: Optional[str] = None) -> Dict:
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"text": text}
    if in_reply_to_tweet_id:
        payload["reply"] = {"in_reply_to_tweet_id": in_reply_to_tweet_id}

    res = requests.post(TWEET_URL, json=payload, headers=headers)
    if res.status_code in (200, 201):
        return res.json()["data"]
    raise Exception(f"Failed to post tweet: {res.status_code} - {res.text}")

def post_tweet_thread(tweets: List[str]) -> List[Dict]:
    if not tweets:
        raise ValueError("No tweets to post.")

    tweet_chain = []
    parent_id = None

    for text in tweets:
        tweet = post_tweet(text, in_reply_to_tweet_id=parent_id)
        tweet_chain.append(tweet)
        parent_id = tweet["id"]  

    return tweet_chain