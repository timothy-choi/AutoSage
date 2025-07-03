import requests

CALENDAR_EVENT_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"

def edit_calendar_event(
    access_token: str,
    calendar_id: str,
    event_id: str,
    summary: str = None,
    description: str = None,
    start_time: str = None,
    end_time: str = None,
    timezone: str = "UTC",
    location: str = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    get_res = requests.get(
        CALENDAR_EVENT_URL.format(calendar_id=calendar_id, event_id=event_id),
        headers=headers
    )
    if get_res.status_code != 200:
        raise Exception(f"Failed to fetch event: {get_res.text}")
    event = get_res.json()

    if summary:
        event["summary"] = summary
    if description:
        event["description"] = description
    if start_time:
        event["start"]["dateTime"] = start_time
        event["start"]["timeZone"] = timezone
    if end_time:
        event["end"]["dateTime"] = end_time
        event["end"]["timeZone"] = timezone
    if location:
        event["location"] = location

    put_res = requests.put(
        CALENDAR_EVENT_URL.format(calendar_id=calendar_id, event_id=event_id),
        headers=headers,
        json=event
    )
    if put_res.status_code != 200:
        raise Exception(f"Failed to update event: {put_res.text}")

    return {
        "status": "success",
        "updated_event": put_res.json()
    }