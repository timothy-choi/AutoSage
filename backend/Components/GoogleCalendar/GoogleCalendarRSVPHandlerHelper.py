import requests

CALENDAR_EVENT_PATCH_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events/{event_id}"

def handle_rsvp(
    access_token: str,
    calendar_id: str,
    event_id: str,
    user_email: str,
    response_status: str  
) -> dict:
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "attendees": [
            {
                "email": user_email,
                "responseStatus": response_status
            }
        ]
    }

    res = requests.patch(
        CALENDAR_EVENT_PATCH_URL.format(calendar_id=calendar_id, event_id=event_id),
        headers=headers,
        json=body,
        params={"sendUpdates": "all"} 
    )

    if res.status_code != 200:
        raise Exception(f"Failed to update RSVP: {res.text}")

    return {
        "status": "success",
        "updated_event": res.json()
    }