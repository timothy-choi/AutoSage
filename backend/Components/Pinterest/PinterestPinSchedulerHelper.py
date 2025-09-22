import requests
import time
import threading

BASE_URL = "https://api.pinterest.com/v5"

def _post_pin(access_token: str, board_id: str, title: str, description: str, media_url: str, link: str = None):
    url = f"{BASE_URL}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "media_source": {
            "source_type": "image_url",
            "url": media_url
        }
    }
    if link:
        data["link"] = link

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def schedule_pin(access_token: str, board_id: str, title: str, description: str, media_url: str, scheduled_time: int, link: str = None):
    def _task():
        delay = scheduled_time - int(time.time())
        if delay > 0:
            time.sleep(delay)
        return _post_pin(access_token, board_id, title, description, media_url, link)

    thread = threading.Thread(target=_task, daemon=True)
    thread.start()
    return {"status": "scheduled", "scheduled_time": scheduled_time}