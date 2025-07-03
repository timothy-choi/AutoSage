import requests
from datetime import datetime
from typing import Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def fetch_upcoming_events(
    access_token: str,
    calendar_id: str = "primary",
    max_results: int = 10,
    query: Optional[str] = None
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "singleEvents": True,
        "orderBy": "startTime",
        "timeMin": datetime.utcnow().isoformat() + "Z",
        "maxResults": max_results
    }

    if query:
        params["q"] = query

    response = requests.get(
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch upcoming events: {response.text}")

    return {
        "status": "success",
        "events": response.json().get("items", [])
    }