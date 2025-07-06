import requests
from datetime import datetime, timedelta
from typing import Optional, List

CALENDAR_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"

def fetch_upcoming_events(
    access_token: str,
    calendar_id: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> List[dict]:
    now = datetime.utcnow()
    time_min = now.isoformat() + "Z"
    time_max = (now + timedelta(hours=hours_ahead)).isoformat() + "Z"

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
        CALENDAR_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if res.status_code != 200:
        raise Exception(f"Failed to fetch calendar events: {res.text}")

    return res.json().get("items", [])

def format_event_summary(event: dict) -> str:
    summary = event.get("summary", "Untitled Event")
    start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    location = event.get("location", "")
    return f"*{summary}*\n🕒 {start}" + (f"\n📍 {location}" if location else "")

def send_to_slack(webhook_url: str, message: str) -> None:
    res = requests.post(webhook_url, json={"text": message})
    if res.status_code != 200:
        raise Exception(f"Slack webhook failed: {res.text}")

def push_calendar_events_to_slack(
    access_token: str,
    calendar_id: str,
    slack_webhook_url: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> dict:
    events = fetch_upcoming_events(
        access_token=access_token,
        calendar_id=calendar_id,
        hours_ahead=hours_ahead,
        max_results=max_results
    )

    if not events:
        send_to_slack(slack_webhook_url, "📅 No upcoming events.")
        return {"status": "success", "message": "No events sent. Empty calendar."}

    formatted_events = "\n\n".join([format_event_summary(e) for e in events])
    slack_message = f"*📅 Upcoming Events ({len(events)} found):*\n\n{formatted_events}"
    send_to_slack(slack_webhook_url, slack_message)

    return {"status": "success", "events_pushed": len(events)}