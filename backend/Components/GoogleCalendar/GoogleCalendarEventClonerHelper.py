import requests

EVENT_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"
EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def fetch_event(access_token: str, calendar_id: str, event_id: str) -> dict:
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(
        EVENT_URL.format(calendar_id=calendar_id, event_id=event_id),
        headers=headers
    )
    if res.status_code != 200:
        raise Exception(f"Failed to fetch event: {res.text}")
    return res.json()

def create_event(access_token: str, calendar_id: str, event_data: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    res = requests.post(
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        json=event_data
    )
    if res.status_code not in (200, 201):
        raise Exception(f"Failed to create event: {res.text}")
    return res.json()

def clone_event(
    access_token: str,
    calendar_id: str,
    event_id: str,
    new_start: str = None,
    new_end: str = None,
    target_calendar_id: str = None
) -> dict:
    event = fetch_event(access_token, calendar_id, event_id)

    for field in ["id", "etag", "htmlLink", "created", "updated", "iCalUID", "sequence", "organizer"]:
        event.pop(field, None)

    if new_start:
        event["start"]["dateTime"] = new_start
    if new_end:
        event["end"]["dateTime"] = new_end

    if target_calendar_id:
        calendar_id = target_calendar_id

    cloned_event = create_event(access_token, calendar_id, event)

    return {
        "status": "success",
        "original_event_id": event_id,
        "cloned_event": cloned_event
    }