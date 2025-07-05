import requests
from datetime import datetime
from typing import Optional

CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def parse_time(t: str) -> datetime:
    return datetime.fromisoformat(t.replace("Z", "+00:00"))

def analyze_meeting_load(
    access_token: str,
    calendar_id: str,
    time_min: str,
    time_max: str,
    max_results: int = 2500
) -> dict:
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
        CALENDAR_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch events: {res.text}")

    events = res.json().get("items", [])
    meeting_durations = []

    for event in events:
        start = event.get("start", {}).get("dateTime")
        end = event.get("end", {}).get("dateTime")

        if not start or not end:
            continue  

        dt_start = parse_time(start)
        dt_end = parse_time(end)
        duration_minutes = (dt_end - dt_start).total_seconds() / 60.0

        if duration_minutes > 0:
            meeting_durations.append(duration_minutes)

    total_meetings = len(meeting_durations)
    total_minutes = sum(meeting_durations)
    avg_minutes = total_minutes / total_meetings if total_meetings > 0 else 0

    return {
        "status": "success",
        "total_meetings": total_meetings,
        "total_minutes": round(total_minutes, 2),
        "average_minutes": round(avg_minutes, 2)
    }