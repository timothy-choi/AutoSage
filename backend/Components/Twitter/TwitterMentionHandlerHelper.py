import os
import requests
from requests_oauthlib import OAuth1
from typing import List, Dict
from datetime import datetime, timedelta

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
MENTIONS_URL = "https://api.twitter.com/1.1/statuses/mentions_timeline.json"

def fetch_recent_mentions(since_id: str = None, count: int = 10) -> List[Dict]:
    params = {"count": count}
    if since_id:
        params["since_id"] = since_id
    response = requests.get(MENTIONS_URL, auth=auth, params=params)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch mentions: {response.status_code} - {response.text}")

def extract_mention_info(tweet: Dict) -> Dict:
    return {
        "user": tweet["user"]["screen_name"],
        "text": tweet["text"],
        "created_at": tweet["created_at"],
        "id_str": tweet["id_str"]
    }

def poll_mentions(interval: int = 30):
    import threading, time
    def poll():
        last_id = None
        while True:
            try:
                mentions = fetch_recent_mentions(last_id)
                if mentions:
                    last_id = mentions[0]["id_str"]
                    for mention in mentions:
                        info = extract_mention_info(mention)
                        print(f"Mention from @{info['user']}: {info['text']}")
            except Exception as e:
                print("Polling error:", e)
            time.sleep(interval)
    thread = threading.Thread(target=poll, daemon=True)
    thread.start()