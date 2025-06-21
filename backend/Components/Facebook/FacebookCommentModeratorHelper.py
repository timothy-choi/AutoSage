import os
import requests
from typing import List, Dict

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")

def list_comments(post_id: str, limit: int = 10) -> List[Dict]:
    url = f"https://graph.facebook.com/v17.0/{post_id}/comments"
    res = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "limit": limit,
        "fields": "id,message,from,created_time,can_hide,is_hidden"
    })
    if res.status_code == 200:
        return res.json().get("data", [])
    raise Exception(f"Failed to list comments: {res.status_code} - {res.text}")

def hide_comment(comment_id: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{comment_id}"
    res = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "is_hidden": "true"
    })
    if res.status_code == 200:
        return "hidden"
    raise Exception(f"Failed to hide comment: {res.status_code} - {res.text}")

def delete_comment(comment_id: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{comment_id}"
    res = requests.delete(url, params={"access_token": PAGE_ACCESS_TOKEN})
    if res.status_code == 200 and res.json().get("success"):
        return "deleted"
    raise Exception(f"Failed to delete comment: {res.status_code} - {res.text}")

def reply_to_comment(comment_id: str, message: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{comment_id}/comments"
    res = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "message": message
    })
    if res.status_code == 200:
        return res.json().get("id")
    raise Exception(f"Failed to reply to comment: {res.status_code} - {res.text}")