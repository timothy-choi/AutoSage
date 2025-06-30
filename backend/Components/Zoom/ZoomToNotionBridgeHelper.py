import requests
from datetime import datetime

def fetch_zoom_meetings(user_id, jwt_token, meeting_type="upcoming"):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {"type": meeting_type, "page_size": 10}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Zoom API error: {response.text}")

    return response.json().get("meetings", [])

def create_notion_page(meeting, database_id, notion_token):
    url = "https://api.notion.com/v1/pages"
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    topic = meeting.get("topic", "Untitled")
    duration = meeting.get("duration", 0)
    start_time = meeting.get("start_time", "")
    join_url = meeting.get("join_url", "")

    # ISO format for Notion Date field
    try:
        date_val = datetime.fromisoformat(start_time.replace("Z", "+00:00")).isoformat()
    except Exception:
        date_val = None

    payload = {
        "parent": {"database_id": database_id},
        "properties": {
            "Name": {
                "title": [{"text": {"content": topic}}]
            },
            "Start Time": {
                "date": {"start": date_val} if date_val else None
            },
            "Duration": {
                "number": duration
            },
            "Join Link": {
                "url": join_url
            }
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    return {
        "status": response.status_code,
        "notion_page_url": response.json().get("url") if response.status_code == 200 else None,
        "error": response.text if response.status_code != 200 else None,
        "topic": topic
    }

def sync_zoom_meetings_to_notion(user_id, zoom_token, notion_token, database_id, meeting_type="upcoming"):
    meetings = fetch_zoom_meetings(user_id, zoom_token, meeting_type)
    results = []

    for meeting in meetings:
        result = create_notion_page(meeting, database_id, notion_token)
        results.append(result)

    return results