import requests
from datetime import datetime, timedelta
from typing import Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def fetch_daily_agenda(
    access_token: str,
    calendar_id: str = "primary",
    timezone: str = "UTC",
    max_results: int = 20
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    now = datetime.utcnow()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)

    params = {
        "timeMin": start_of_day.isoformat() + "Z",
        "timeMax": end_of_day.isoformat() + "Z",
        "singleEvents": True,
        "orderBy": "startTime",
        "maxResults": max_results
    }

    res = requests.get(
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch today's agenda: {res.text}")

    events = res.json().get("items", [])

    agenda = []
    for event in events:
        agenda.append({
            "summary": event.get("summary", "Untitled Event"),
            "start": event.get("start", {}).get("dateTime", event.get("start", {}).get("date")),
            "end": event.get("end", {}).get("dateTime", event.get("end", {}).get("date"))
        })

    return {
        "status": "success",
        "agenda": agenda
    }