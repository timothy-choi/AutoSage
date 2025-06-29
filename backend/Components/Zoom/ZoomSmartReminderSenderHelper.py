import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def fetch_upcoming_meetings(user_id, jwt_token):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {
        "type": "upcoming",
        "page_size": 30
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch meetings: {response.text}")

    return response.json().get("meetings", [])

def filter_meetings_within_timeframe(meetings, minutes_ahead, timezone="UTC"):
    now = datetime.now(ZoneInfo(timezone))
    cutoff = now + timedelta(minutes=minutes_ahead)

    upcoming = []
    for m in meetings:
        start_time_str = m.get("start_time")
        if not start_time_str:
            continue

        try:
            start_dt = datetime.fromisoformat(start_time_str.replace("Z", "+00:00"))
            if now <= start_dt <= cutoff:
                upcoming.append(m)
        except Exception:
            continue

    return upcoming

def send_reminder(meeting, sender="console", webhook_url=None):
    topic = meeting.get("topic", "Untitled")
    start_time = meeting.get("start_time", "Unknown")
    join_url = meeting.get("join_url", "")
    message = f"🔔 Reminder: '{topic}' starts at {start_time}. Join: {join_url}"

    if sender == "console":
        print(message)
        return {"status": "printed", "message": message}
    elif sender == "webhook" and webhook_url:
        response = requests.post(webhook_url, json={"text": message})
        return {
            "status": "sent" if response.status_code == 200 else "failed",
            "message": message,
            "code": response.status_code
        }
    else:
