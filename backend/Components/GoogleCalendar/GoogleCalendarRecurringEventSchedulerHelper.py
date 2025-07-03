import requests

CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def create_recurring_event(
    access_token: str,
    calendar_id: str,
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    timezone: str,
    rrule: str,
    location: str = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    event_data = {
        "summary": summary,
        "description": description,
        "start": {
            "dateTime": start_time,
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_time,
            "timeZone": timezone
        },
        "recurrence": [rrule]
    }

    if location:
        event_data["location"] = location

    res = requests.post(
        CALENDAR_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        json=event_data
    )

    if res.status_code not in (200, 201):
        raise Exception(f"Failed to create recurring event: {res.text}")

    return {
        "status": "success",
        "event": res.json()
    }