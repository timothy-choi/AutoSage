import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

def fetch_upcoming_zoom_meetings(user_id, jwt_token):
    url = f"https://api.zoom.us/v2/users/{user_id}/meetings"
    headers = {"Authorization": f"Bearer {jwt_token}"}
    params = {"type": "upcoming", "page_size": 20}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Zoom meetings: {response.text}")

    return response.json().get("meetings", [])

def create_google_calendar_event(zoom_meeting, calendar_id, google_token, timezone="UTC"):
    start_time = zoom_meeting.get("start_time")
    duration_min = zoom_meeting.get("duration", 30)
    topic = zoom_meeting.get("topic", "Zoom Meeting")
    join_url = zoom_meeting.get("join_url")

    start_dt = datetime.fromisoformat(start_time.replace("Z", "+00:00")).astimezone(ZoneInfo(timezone))
    end_dt = start_dt + timedelta(minutes=duration_min)

    url = f"https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
    headers = {
        "Authorization": f"Bearer {google_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "summary": topic,
        "description": f"Zoom Link: {join_url}",
        "start": {
            "dateTime": start_dt.isoformat(),
            "timeZone": timezone
        },
        "end": {
            "dateTime": end_dt.isoformat(),
            "timeZone": timezone
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    return {
        "zoom_meeting_id": zoom_meeting.get("id"),
        "google_event_status": response.status_code,
        "google_event_id": response.json().get("id") if response.status_code == 200 else None,
        "error": response.text if response.status_code != 200 else None
    }

def sync_zoom_to_google_calendar(user_id, jwt_token, calendar_id, google_token, timezone="UTC"):
    meetings = fetch_upcoming_zoom_meetings(user_id, jwt_token)
    results = []
    for meeting in meetings:
        result = create_google_calendar_event(meeting, calendar_id, google_token, timezone)
        results.append(result)
    return results