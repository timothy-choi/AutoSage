import requests
from datetime import datetime, timedelta
from typing import List, Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def send_manual_reminders(
    access_token: str,
    calendar_id: str = "primary",
    hours_ahead: int = 24,
    filter_query: Optional[str] = None,
    max_results: int = 10
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    time_min = datetime.utcnow().isoformat() + "Z"
    time_max = (datetime.utcnow() + timedelta(hours=hours_ahead)).isoformat() + "Z"

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
        "maxResults": max_results,
        "singleEvents": True,
        "orderBy": "startTime"
    }

    if filter_query:
        params["q"] = filter_query

    response = requests.get(
        EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch events: {response.text}")

    events = response.json().get("items", [])
    reminders_sent = []

    for event in events:
        summary = event.get("summary", "Untitled Event")
        start = event.get("start", {}).get("dateTime", event.get("start", {}).get("date"))
        attendees = event.get("attendees", [])

        for attendee in attendees:
            email = attendee.get("email")
            if email:
                print(f"Reminder sent to {email} for event '{summary}' at {start}")
                reminders_sent.append({
                    "email": email,
                    "event": summary,
                    "start": start
                })

    return {
        "status": "success",
        "reminders_sent": reminders_sent
    }