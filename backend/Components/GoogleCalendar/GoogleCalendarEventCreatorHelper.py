import requests

CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def create_calendar_event(
    access_token: str,
    calendar_id: str,
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    timezone: str = "UTC",
    location: str = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone
        }
    }

    if location:
        payload["location"] = location

    url = CALENDAR_EVENTS_URL.format(calendar_id=calendar_id)

    res = requests.post(url, headers=headers, json=payload)
    if res.status_code not in (200, 201):
        raise Exception(f"Failed to create event: {res.text}")

    return {
        "status": "success",
        "event": res.json()
    }