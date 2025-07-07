import requests
from datetime import datetime, timedelta
from typing import List, Optional

FREEBUSY_URL = "https://www.googleapis.com/calendar/v3/freeBusy"
EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def find_next_free_slot(
    access_token: str,
    calendar_id: str,
    duration_minutes: int,
    earliest_start_utc: Optional[str] = None,
    latest_end_utc: Optional[str] = None
) -> Optional[tuple]:
    now = datetime.utcnow()
    time_min = earliest_start_utc or (now + timedelta(minutes=15)).isoformat() + "Z"
    time_max = latest_end_utc or (now + timedelta(days=2)).isoformat() + "Z"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": calendar_id}]
    }

    response = requests.post(FREEBUSY_URL, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception(f"FreeBusy query failed: {response.text}")

    busy_times = response.json()["calendars"][calendar_id]["busy"]

    start_time = datetime.fromisoformat(time_min.replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(time_max.replace("Z", "+00:00"))
    meeting_delta = timedelta(minutes=duration_minutes)

    pointer = start_time
    for busy in busy_times:
        busy_start = datetime.fromisoformat(busy["start"].replace("Z", "+00:00"))
        if pointer + meeting_delta <= busy_start:
            return pointer.isoformat(), (pointer + meeting_delta).isoformat()
        pointer = max(pointer, datetime.fromisoformat(busy["end"].replace("Z", "+00:00")))

    if pointer + meeting_delta <= end_time:
        return pointer.isoformat(), (pointer + meeting_delta).isoformat()

    return None

def create_calendar_event(
    access_token: str,
    calendar_id: str,
    start_time_iso: str,
    end_time_iso: str,
    title: str,
    description: Optional[str] = None,
    location: Optional[str] = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "summary": title,
        "description": description or "",
        "location": location or "",
        "start": {"dateTime": start_time_iso, "timeZone": "UTC"},
        "end": {"dateTime": end_time_iso, "timeZone": "UTC"}
    }

    res = requests.post(EVENTS_URL.format(calendar_id=calendar_id), headers=headers, json=payload)
    if res.status_code != 200:
        raise Exception(f"Failed to create event: {res.text}")

    return res.json()

def smart_schedule_event(
    access_token: str,
    calendar_id: str,
    duration_minutes: int,
    title: str,
    description: Optional[str] = None,
    location: Optional[str] = None,
    earliest_start_utc: Optional[str] = None,
    latest_end_utc: Optional[str] = None
) -> dict:
    slot = find_next_free_slot(
        access_token=access_token,
        calendar_id=calendar_id,
        duration_minutes=duration_minutes,
        earliest_start_utc=earliest_start_utc,
        latest_end_utc=latest_end_utc
    )

    if not slot:
        return {"status": "failed", "message": "No available slots found."}

    start_time, end_time = slot
    event = create_calendar_event(
        access_token,
        calendar_id,
        start_time,
        end_time,
        title,
        description,
        location
    )

    return {
        "status": "scheduled",
        "event_id": event["id"],
        "summary": event["summary"],
        "start": start_time,
        "end": end_time,
        "htmlLink": event.get("htmlLink")
    }