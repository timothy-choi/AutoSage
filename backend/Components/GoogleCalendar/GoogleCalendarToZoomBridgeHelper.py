import requests
from datetime import datetime, timedelta
from typing import List

GOOGLE_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
ZOOM_MEETING_URL = "https://api.zoom.us/v2/users/me/meetings"

def fetch_upcoming_events(
    access_token: str,
    calendar_id: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> List[dict]:
    now = datetime.utcnow()
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(hours=hours_ahead)).isoformat() + "Z"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": max_results
    }

    res = requests.get(
        GOOGLE_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch calendar events: {res.text}")

    return res.json().get("items", [])

def create_zoom_meeting(event: dict, zoom_jwt_token: str) -> dict:
    headers = {
        "Authorization": f"Bearer {zoom_jwt_token}",
        "Content-Type": "application/json"
    }

    topic = event.get("summary", "Untitled Event")
    start_time = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    duration_minutes = 60  
    description = event.get("description", "")

    payload = {
        "topic": topic,
        "type": 2,  
        "start_time": start_time,
        "duration": duration_minutes,
        "timezone": "UTC",
        "agenda": description,
        "settings": {
            "join_before_host": True,
            "mute_upon_entry": True
        }
    }

    res = requests.post(ZOOM_MEETING_URL, headers=headers, json=payload)
    if res.status_code != 201:
        raise Exception(f"Failed to create Zoom meeting: {res.text}")

    return res.json()

def push_calendar_events_to_zoom(
    google_access_token: str,
    calendar_id: str,
    zoom_jwt_token: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> dict:
    events = fetch_upcoming_events(
        access_token=google_access_token,
        calendar_id=calendar_id,
        hours_ahead=hours_ahead,
        max_results=max_results
    )

    results = []
    for event in events:
        try:
            zoom_meeting = create_zoom_meeting(event, zoom_jwt_token)
            results.append({
                "event": event.get("summary"),
                "zoom_meeting_id": zoom_meeting.get("id"),
                "zoom_join_url": zoom_meeting.get("join_url")
            })
        except Exception as e:
            results.append({
                "event": event.get("summary"),
                "error": str(e)
            })

    return {
        "status": "completed",
        "created": len(results),
        "details": results
    }