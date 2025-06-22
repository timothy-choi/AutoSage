import os
import requests
from typing import Optional, Dict
from TwitterTweetPublisherHelper import post_tweet

TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")

def delete_tweet(tweet_id: str) -> Dict:
    url = f"https://api.twitter.com/2/tweets/{tweet_id}"
    headers = {
        "Authorization": f"Bearer {TWITTER_BEARER_TOKEN}"
    }

    res = requests.delete(url, headers=headers)
    if res.status_code == 200:
        return {"status": "deleted", "tweet_id": tweet_id}
    raise Exception(f"Failed to delete tweet: {res.status_code} - {res.text}")

def simulate_edit_tweet(tweet_id: str, new_text: str, media_id: Optional[str] = None) -> Dict:
    deleted = delete_tweet(tweet_id)
    new_text = new_text.strip() + " [Edited]"
    posted = post_tweet(new_text, media_id)
    return {
        "original_tweet_deleted": deleted,
        "reposted_tweet": posted
    }