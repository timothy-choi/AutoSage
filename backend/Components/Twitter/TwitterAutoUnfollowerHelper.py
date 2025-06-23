import os
import requests
from requests_oauthlib import OAuth1
from typing import List, Dict

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")

auth = OAuth1(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)
FRIENDS_URL = "https://api.twitter.com/1.1/friends/ids.json"
FOLLOWERS_URL = "https://api.twitter.com/1.1/followers/ids.json"
UNFOLLOW_URL_TEMPLATE = "https://api.twitter.com/1.1/friendships/destroy.json?user_id={}"  # POST


def get_following_ids(screen_name: str) -> List[int]:
    params = {"screen_name": screen_name, "stringify_ids": True, "count": 5000}
    res = requests.get(FRIENDS_URL, auth=auth, params=params)
    if res.status_code == 200:
        return res.json().get("ids", [])
    raise Exception(f"Failed to fetch following IDs: {res.status_code} - {res.text}")


def get_follower_ids(screen_name: str) -> List[int]:
    params = {"screen_name": screen_name, "stringify_ids": True, "count": 5000}
    res = requests.get(FOLLOWERS_URL, auth=auth, params=params)
    if res.status_code == 200:
        return res.json().get("ids", [])
    raise Exception(f"Failed to fetch follower IDs: {res.status_code} - {res.text}")


def get_non_followers(screen_name: str) -> List[int]:
    following = set(get_following_ids(screen_name))
    followers = set(get_follower_ids(screen_name))
    return list(following - followers)


def unfollow_users(user_ids: List[int]) -> List[Dict]:
    results = []
    for uid in user_ids:
        url = UNFOLLOW_URL_TEMPLATE.format(uid)
        res = requests.post(url, auth=auth)
        results.append({"user_id": uid, "status": res.status_code, "message": res.reason})
    return results


def auto_unfollow_nonfollowers(screen_name: str, limit: int = 10) -> Dict:
    nonfollowers = get_non_followers(screen_name)
    to_unfollow = nonfollowers[:limit]
    results = unfollow_users(to_unfollow)
    return {
        "attempted": len(to_unfollow),
        "unfollowed": results
    }