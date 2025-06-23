import os
import requests
from requests_oauthlib import OAuth1
from typing import List, Dict

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
LIKES_URL = "https://api.twitter.com/1.1/favorites/list.json"
RETWEETS_URL_TEMPLATE = "https://api.twitter.com/1.1/statuses/retweets/{tweet_id}.json"


def fetch_recent_likes(screen_name: str, count: int = 10) -> List[Dict]:
    params = {"screen_name": screen_name, "count": count}
    response = requests.get(LIKES_URL, auth=auth, params=params)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch likes: {response.status_code} - {response.text}")


def fetch_retweets(tweet_id: str, count: int = 10) -> List[Dict]:
    url = RETWEETS_URL_TEMPLATE.format(tweet_id=tweet_id)
    params = {"count": count}
    response = requests.get(url, auth=auth, params=params)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch retweets: {response.status_code} - {response.text}")


def summarize_likes(likes: List[Dict]) -> List[Dict]:
    return [
        {
            "user": like["user"]["screen_name"],
            "tweet": like["text"],
            "liked_at": like["created_at"]
        }
        for like in likes
    ]


def summarize_retweets(retweets: List[Dict]) -> List[Dict]:
    return [
        {
            "user": rt["user"]["screen_name"],
            "retweeted_at": rt["created_at"],
            "original_tweet": rt["text"]
        }
        for rt in retweets
    ]