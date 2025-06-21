import os
import json
import threading
import time
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
FEED_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}/feed"
PHOTO_URL = f"https://graph.facebook.com/v17.0/{PAGE_ID}/photos"

SCHEDULED_LOG_FILE = "logs/facebook_scheduled_posts.jsonl"
os.makedirs("logs", exist_ok=True)

def log_scheduled_post(data: dict):
    with open(SCHEDULED_LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")

def schedule_text_post(message: str, scheduled_time: str) -> str:
    def send_later():
        now = datetime.now()
        post_time = datetime.fromisoformat(scheduled_time)
        delay = (post_time - now).total_seconds()
        if delay > 0:
            time.sleep(delay)
        try:
            requests.post(
                FEED_URL,
                params={
                    "access_token": PAGE_ACCESS_TOKEN,
                    "message": message
                }
            )
        except Exception as e:
            print(f"[Text Post Scheduler] Error: {e}")

    log_scheduled_post({
        "type": "text",
        "message": message,
        "scheduled_time": scheduled_time,
        "status": "scheduled"
    })

    thread = threading.Thread(target=send_later)
    thread.start()
    return "scheduled"

def schedule_photo_post(image_url: str, caption: str, scheduled_time: str) -> str:
    def send_later():
        now = datetime.now()
        post_time = datetime.fromisoformat(scheduled_time)
        delay = (post_time - now).total_seconds()
        if delay > 0:
            time.sleep(delay)
        try:
            requests.post(
                PHOTO_URL,
                params={
                    "access_token": PAGE_ACCESS_TOKEN,
                    "url": image_url,
                    "caption": caption,
                    "published": "true"
                }
            )
        except Exception as e:
            print(f"[Photo Post Scheduler] Error: {e}")

    log_scheduled_post({
        "type": "photo",
        "image_url": image_url,
        "caption": caption,
        "scheduled_time": scheduled_time,
        "status": "scheduled"
    })

    thread = threading.Thread(target=send_later)
    thread.start()
    return "scheduled"