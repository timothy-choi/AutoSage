import os
import json
import requests
from typing import List, Dict
from datetime import datetime, timedelta

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
FEED_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}/posts"
BACKUP_FILE = "logs/facebook_post_backups.jsonl"
os.makedirs("logs", exist_ok=True)

def delete_facebook_post(post_id: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{post_id}"
    res = requests.delete(url, params={"access_token": PAGE_ACCESS_TOKEN})
    if res.status_code == 200 and res.json().get("success"):
        return "deleted"
    raise Exception(f"Failed to delete post: {res.status_code} - {res.text}")

def get_facebook_post(post_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{post_id}"
    res = requests.get(url, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "fields": "id,message,created_time"
    })
    if res.status_code == 200:
        return res.json()
    raise Exception(f"Failed to fetch post: {res.status_code} - {res.text}")

def soft_delete_post(post_id: str) -> str:
    post_data = get_facebook_post(post_id)
    with open(BACKUP_FILE, "a") as f:
        f.write(json.dumps(post_data) + "\n")
    return delete_facebook_post(post_id)

def undo_deleted_post(post_data: Dict) -> str:
    res = requests.post(
        f"https://graph.facebook.com/v17.0/{PAGE_ID}/feed",
        params={"access_token": PAGE_ACCESS_TOKEN, "message": post_data.get("message", "Restored post")}
    )
    if res.status_code == 200:
        return res.json().get("id")
    raise Exception(f"Failed to restore post: {res.status_code} - {res.text}")

def delete_multiple_posts(post_ids: List[str]) -> List[Dict]:
    results = []
    for pid in post_ids:
        try:
            result = delete_facebook_post(pid)
            results.append({"post_id": pid, "status": result})
        except Exception as e:
            results.append({"post_id": pid, "error": str(e)})
    return results

def list_facebook_posts(limit: int = 100) -> List[Dict]:
    res = requests.get(FEED_URL, params={
        "access_token": PAGE_ACCESS_TOKEN,
        "limit": limit,
        "fields": "id,message,created_time"
    })
    if res.status_code == 200:
        return res.json().get("data", [])
    raise Exception(f"Failed to list posts: {res.status_code} - {res.text}")

def delete_posts_by_keyword(keyword: str) -> List[str]:
    deleted = []
    posts = list_facebook_posts(limit=100)
    for post in posts:
        if keyword.lower() in (post.get("message") or "").lower():
            try:
                delete_facebook_post(post["id"])
                deleted.append(post["id"])
            except:
                continue
    return deleted

def delete_old_posts(days_old: int) -> List[str]:
    deleted = []
    cutoff = datetime.utcnow() - timedelta(days=days_old)
    posts = list_facebook_posts(limit=100)
    for post in posts:
        created = post.get("created_time")
        if created:
            post_time = datetime.fromisoformat(created.replace("Z", "+00:00"))
            if post_time < cutoff:
                try:
                    delete_facebook_post(post["id"])
                    deleted.append(post["id"])
                except:
                    continue
    return deleted