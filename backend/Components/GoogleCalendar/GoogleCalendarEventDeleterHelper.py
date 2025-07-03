import requests
from datetime import datetime

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
EVENT_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"

def list_events(
    access_token: str,
    calendar_id: str,
    time_max: str = None,
    q: str = None,
    max_results: int = 250
) -> list:
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {
        "maxResults": max_results,
        "singleEvents": True,
        "orderBy": "startTime",
        "fields": "items(id,summary,start,end)"
    }
    if time_max:
        params["timeMax"] = time_max
    if q:
        params["q"] = q

    res = requests.get(EVENTS_URL.format(calendar_id=calendar_id), headers=headers, params=params)
    if res.status_code != 200:
        raise Exception(f"Failed to list events: {res.text}")
    return res.json().get("items", [])

def delete_event(access_token: str, calendar_id: str, event_id: str) -> None:
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.delete(EVENT_URL.format(calendar_id=calendar_id, event_id=event_id), headers=headers)
    if res.status_code not in (200, 204):
        raise Exception(f"Failed to delete event {event_id}: {res.text}")

def batch_delete_events(
    access_token: str,
    calendar_id: str,
    time_max: str = None,
    q: str = None
) -> dict:
    events = list_events(access_token, calendar_id, time_max, q)
    deleted = []
    for e in events:
        delete_event(access_token, calendar_id, e["id"])
        deleted.append(e["id"])
    return {
        "status": "success",
        "deleted_count": len(deleted),
        "deleted_event_ids": deleted
    }