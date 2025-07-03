import requests

MOVE_EVENT_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}/move"

def move_calendar_event(
    access_token: str,
    source_calendar_id: str,
    event_id: str,
    target_calendar_id: str
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    params = {
        "destination": target_calendar_id
    }

    res = requests.post(
        MOVE_EVENT_URL.format(calendar_id=source_calendar_id, event_id=event_id),
        headers=headers,
        params=params
    )

    if res.status_code not in (200, 201):
        raise Exception(f"Failed to move event: {res.text}")

    return {
        "status": "success",
        "moved_event": res.json()
    }