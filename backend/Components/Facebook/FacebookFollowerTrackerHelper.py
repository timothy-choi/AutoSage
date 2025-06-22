import os
import requests
from typing import Dict, List
from datetime import datetime

ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def fetch_follower_count(page_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{page_id}?fields=followers_count&access_token={ACCESS_TOKEN}"
    res = requests.get(url)

    if res.status_code == 200:
        count = res.json().get("followers_count", 0)
        return {
            "followers": count,
            "timestamp": datetime.now().isoformat()
        }
    raise Exception(f"Failed to fetch followers: {res.status_code} - {res.text}")

def fetch_daily_followers(page_id: str, days: int = 7) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{page_id}/insights"
    params = {
        "metric": "page_fan_adds_unique",
        "period": "day",
        "access_token": ACCESS_TOKEN
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        values = res.json().get("data", [])[0].get("values", [])
        return {v["end_time"]: v["value"] for v in values[-days:]}
    raise Exception(f"Failed to fetch daily followers: {res.status_code} - {res.text}")

def fetch_page_info_with_followers(page_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{page_id}?fields=name,followers_count&access_token={ACCESS_TOKEN}"
    res = requests.get(url)
    if res.status_code == 200:
        data = res.json()
        return {
            "page_name": data["name"],
            "followers": data["followers_count"],
            "timestamp": datetime.now().isoformat()
        }
    raise Exception("Failed to fetch page info")