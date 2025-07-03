import requests
from typing import Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def fetch_calendar_events(
    access_token: str,
    calendar_id: str = "primary",
    time_min: Optional[str] = None,
    time_max: Optional[str] = None,
    query: Optional[str] = None,
    max_results: int = 50
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "maxResults": max_results,
        "singleEvents": True,
        "orderBy": "startTime"
    }

    if time_min:
        params["timeMin"] = time_min
    if time_max:
        params["timeMax"] = time_max
    if query:
        params["q"] = query

    res = requests.get(
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch events: {res.text}")

    return {
        "status": "success",
        "events": res.json().get("items", [])
    }