import requests
from datetime import datetime
from typing import List, Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def parse_iso_time(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))

def events_overlap(event1: dict, event2: dict) -> bool:
    start1 = parse_iso_time(event1['start']['dateTime'])
    end1 = parse_iso_time(event1['end']['dateTime'])
    start2 = parse_iso_time(event2['start']['dateTime'])
    end2 = parse_iso_time(event2['end']['dateTime'])
    return max(start1, start2) < min(end1, end2)

def detect_overlapping_events(
    access_token: str,
    calendar_id: str,
    time_min: str,
    time_max: str,
    max_results: int = 50
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
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch events: {res.text}")

    events = res.json().get("items", [])

    overlaps = []
    for i in range(len(events)):
        for j in range(i + 1, len(events)):
            e1 = events[i]
            e2 = events[j]
            if 'dateTime' not in e1.get('start', {}) or 'dateTime' not in e2.get('start', {}):
                continue  
            if events_overlap(e1, e2):
                overlaps.append({
                    "event_1": {
                        "id": e1.get("id"),
                        "summary": e1.get("summary"),
                        "start": e1["start"]["dateTime"],
                        "end": e1["end"]["dateTime"]
                    },
                    "event_2": {
                        "id": e2.get("id"),
                        "summary": e2.get("summary"),
                        "start": e2["start"]["dateTime"],
                        "end": e2["end"]["dateTime"]
                    }
                })