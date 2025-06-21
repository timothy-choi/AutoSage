import os
import requests
from typing import List, Dict

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def fetch_comments(post_id: str, limit: int = 10) -> List[Dict]:
    url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
    res = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "limit": limit,
        "fields": "id,message,from,created_time,comment_count"
    })
    if res.status_code == 200:
        return res.json().get("data", [])
    raise Exception(f"Failed to fetch comments: {res.status_code} - {res.text}")

def fetch_comment_replies(comment_id: str, limit: int = 10) -> List[Dict]:
    url = f"https://graph.facebook.com/v17.0/{comment_id}/comments"
    res = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "limit": limit,
        "fields": "id,message,from,created_time"
    })
    if res.status_code == 200:
        return res.json().get("data", [])
    raise Exception(f"Failed to fetch replies: {res.status_code} - {res.text}")