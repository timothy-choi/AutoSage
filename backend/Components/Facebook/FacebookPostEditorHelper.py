import os
import requests
from typing import List, Dict

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")

def edit_facebook_post(post_id: str, new_message: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{post_id}"
    response = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "message": new_message
    })
    if response.status_code == 200:
        return "edited"
    raise Exception(f"Edit error: {response.status_code} - {response.text}")

def delete_facebook_post(post_id: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{post_id}"
    response = requests.delete(url, params={
        "access_token": PAGE_ACCESS_TOKEN
    })
    if response.status_code == 200 and response.json().get("success"):
        return "deleted"
    raise Exception(f"Delete error: {response.status_code} - {response.text}")

def get_facebook_post(post_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{post_id}"
    response = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "fields": "message,created_time,id"
    })
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Fetch error: {response.status_code} - {response.text}")

def list_facebook_posts(limit: int = 10) -> List[Dict]:
    url = f"https://graph.facebook.com/v17.0/{PAGE_ID}/posts"
    response = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "limit": limit,
        "fields": "id,message,created_time"
    })
    if response.status_code == 200:
        return response.json().get("data", [])
    raise Exception(f"List error: {response.status_code} - {response.text}")

def restore_facebook_post(post_data: Dict) -> str:
    url = f"https://graph.facebook.com/v17.0/{PAGE_ID}/feed"
    response = requests.post(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "message": post_data.get("message", "Restored post")
    })
    if response.status_code == 200:
        return response.json().get("id")
    raise Exception(f"Restore error: {response.status_code} - {response.text}")

def bulk_edit_posts(edits: List[Dict[str, str]]) -> List[str]:
    results = []
    for edit in edits:
        post_id = edit.get("post_id")
        new_msg = edit.get("new_message")
        try:
            result = edit_facebook_post(post_id, new_msg)
            results.append(f"{post_id}: {result}")
        except Exception as e:
            results.append(f"{post_id}: failed - {str(e)}")
    return results