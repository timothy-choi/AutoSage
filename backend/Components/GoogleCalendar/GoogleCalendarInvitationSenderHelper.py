import requests
from typing import List, Optional

CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def send_calendar_invitation(
    access_token: str,
    calendar_id: str,
    summary: str,
    description: str,
    start_time: str,
    end_time: str,
    timezone: str,
    attendees: List[str],
    location: Optional[str] = None
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
        "attendees": [{"email": email} for email in attendees],
        "sendUpdates": "all"
    }

    if location:
        event_data["location"] = location

    response = requests.post(
        CALENDAR_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        json=event_data
    )

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to send calendar invitation: {response.text}")

    return {
        "status": "success",
        "event": response.json()
    }