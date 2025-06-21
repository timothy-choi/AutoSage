import os
import requests

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")

TEXT_POST_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}/feed"
PHOTO_POST_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}/photos"

def publish_facebook_post(message: str) -> str:
    if not PAGE_ACCESS_TOKEN or not PAGE_ID:
        raise ValueError("Missing FB_PAGE_ACCESS_TOKEN or FB_PAGE_ID.")

    response = requests.post(
        TEXT_POST_URL,
        params={"access_token": PAGE_ACCESS_TOKEN, "message": message}
    )

    if response.status_code == 200:
        return response.json().get("id")
    else:
        raise Exception(f"Facebook API error: {response.status_code} - {response.text}")

def publish_photo_post(image_url: str, caption: str) -> str:
    if not PAGE_ACCESS_TOKEN or not PAGE_ID:
        raise ValueError("Missing FB_PAGE_ACCESS_TOKEN or FB_PAGE_ID.")

    response = requests.post(
        PHOTO_POST_URL,
        params={
            "access_token": PAGE_ACCESS_TOKEN,
            "url": image_url,
            "caption": caption,
            "published": "true"
        }
    )

    if response.status_code == 200:
        return response.json().get("post_id")
    else:
        raise Exception(f"Facebook API photo post error: {response.status_code} - {response.text}")