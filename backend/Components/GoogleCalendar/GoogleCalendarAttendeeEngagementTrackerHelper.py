import requests
from typing import Optional

EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def track_attendee_engagement(
    access_token: str,
    calendar_id: str,
    attendee_email: str,
    time_min: str,
    time_max: str,
    max_results: int = 2500
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    params = {
        "timeMin": time_min,
        "timeMax": time_max,
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
        raise Exception(f"Failed to fetch calendar events: {res.text}")

    events = res.json().get("items", [])
    
    total_invited = 0
    accepted = 0
    declined = 0
    tentative = 0
    no_response = 0

    for event in events:
        attendees = event.get("attendees", [])
        for att in attendees:
            if att.get("email") == attendee_email:
                total_invited += 1
                status = att.get("responseStatus", "needsAction")
                if status == "accepted":
                    accepted += 1
                elif status == "declined":
                    declined += 1
                elif status == "tentative":
                    tentative += 1
                elif status == "needsAction":
                    no_response += 1

    acceptance_rate = (accepted / total_invited) * 100 if total_invited else 0.0

    return {
        "status": "success",
        "attendee_email": attendee_email,
        "total_invited": total_invited,
        "accepted": accepted,
        "declined": declined,
        "tentative": tentative,
        "no_response": no_response,
        "acceptance_rate": round(acceptance_rate, 2)
    }