import requests
from datetime import datetime, timedelta
from typing import Optional

GOOGLE_FREEBUSY_URL = "https://www.googleapis.com/calendar/v3/freeBusy"
GOOGLE_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def find_free_block(
    access_token: str,
    calendar_id: str,
    duration_minutes: int,
    start_from: Optional[str] = None,
    end_by: Optional[str] = None
) -> Optional[tuple]:
    now = datetime.utcnow()
    time_min = start_from or (now + timedelta(minutes=15)).isoformat() + "Z"
    time_max = end_by or (now + timedelta(days=1)).isoformat() + "Z"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": calendar_id}]
    }

    res = requests.post(GOOGLE_FREEBUSY_URL, headers=headers, json=body)
    if res.status_code != 200:
        raise Exception(f"FreeBusy lookup failed: {res.text}")

    busy_slots = res.json()["calendars"][calendar_id]["busy"]
    start = datetime.fromisoformat(time_min.replace("Z", "+00:00"))
    end = datetime.fromisoformat(time_max.replace("Z", "+00:00"))
    block_delta = timedelta(minutes=duration_minutes)

    pointer = start
    for slot in busy_slots:
        busy_start = datetime.fromisoformat(slot["start"].replace("Z", "+00:00"))
        if pointer + block_delta <= busy_start:
            return pointer.isoformat(), (pointer + block_delta).isoformat()
        pointer = max(pointer, datetime.fromisoformat(slot["end"].replace("Z", "+00:00")))

    if pointer + block_delta <= end:
        return pointer.isoformat(), (pointer + block_delta).isoformat()

    return None

def create_block_event(
    access_token: str,
    calendar_id: str,
    start_time: str,
    end_time: str,
    title: str = "🛡️ Focus Block",
    description: Optional[str] = "Auto-blocked time"
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    event = {
        "summary": title,
        "description": description,
        "start": {"dateTime": start_time, "timeZone": "UTC"},
        "end": {"dateTime": end_time, "timeZone": "UTC"},
        "transparency": "opaque",
        "visibility": "private"
    }

    res = requests.post(GOOGLE_EVENTS_URL.format(calendar_id=calendar_id), headers=headers, json=event)
    if res.status_code != 200:
        raise Exception(f"Failed to create block event: {res.text}")

    return res.json()

def auto_block_time(
    access_token: str,
    calendar_id: str,
    duration_minutes: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    start_from: Optional[str] = None,
    end_by: Optional[str] = None
) -> dict:
    slot = find_free_block(access_token, calendar_id, duration_minutes, start_from, end_by)

    if not slot:
        return {"status": "failed", "message": "No free slot found."}

    start_time, end_time = slot
    event = create_block_event(
        access_token,
        calendar_id,
        start_time,
        end_time,
        title or "🛡️ Focus Block",
        description
    )

    return {
        "status": "blocked",
        "event_id": event["id"],
        "start": start_time,
        "end": end_time,
        "link": event.get("htmlLink")
    }