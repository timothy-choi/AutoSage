import requests
from typing import List

FREEBUSY_URL = "https://www.googleapis.com/calendar/v3/freeBusy"

def check_attendee_availability(
    access_token: str,
    attendee_emails: List[str],
    time_min: str,
    time_max: str
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "timeMin": time_min,
        "timeMax": time_max,
        "items": [{"id": email} for email in attendee_emails]
    }

    response = requests.post(FREEBUSY_URL, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception(f"Failed to check attendee availability: {response.text}")

    calendars = response.json().get("calendars", {})

    results = {}
    for email, data in calendars.items():
        results[email] = {
            "busy_blocks": data.get("busy", []),
            "is_available": len(data.get("busy", [])) == 0
        }

    return {
        "status": "success",
        "availability": results
    }