import os
import requests
from typing import Optional, Dict

ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
IG_BUSINESS_ACCOUNT_ID = os.getenv("IG_BUSINESS_ACCOUNT_ID")  

def create_instagram_media(image_url: str, caption: str) -> str:
    url = f"https://graph.facebook.com/v17.0/{IG_BUSINESS_ACCOUNT_ID}/media"
    params = {
        "image_url": image_url,
        "caption": caption,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, data=params)
    if res.status_code == 200:
        return res.json().get("id")
    raise Exception(f"Instagram media creation failed: {res.text}")

def publish_instagram_media(container_id: str) -> Dict:
    url = f"https://graph.facebook.com/v17.0/{IG_BUSINESS_ACCOUNT_ID}/media_publish"
    params = {
        "creation_id": container_id,
        "access_token": ACCESS_TOKEN
    }
    res = requests.post(url, data=params)
    if res.status_code == 200:
        return res.json()
    raise Exception(f"Instagram publish failed: {res.text}")

def cross_post_facebook_to_instagram(fb_post: Dict) -> Dict:
    container_id = create_instagram_media(
        image_url=fb_post["image_url"],
        caption=fb_post.get("caption", "")
    )
    return publish_instagram_media(container_id)