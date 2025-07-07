import requests
from datetime import datetime, timedelta
from typing import List

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

    response = requests.get(
        CALENDAR_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch calendar events: {response.text}")

    return response.json().get("items", [])

def format_event(event: dict) -> str:
    summary = event.get("summary", "Untitled Event")
    start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    location = event.get("location", "")
    return f"📌 **{summary}**\n🕒 `{start}`" + (f"\n📍 *{location}*" if location else "")

def post_to_discord(webhook_url: str, content: str):
    res = requests.post(webhook_url, json={"content": content})
    if res.status_code != 204 and res.status_code != 200:
        raise Exception(f"Failed to post to Discord: {res.status_code} - {res.text}")

def push_calendar_events_to_discord(
    access_token: str,
    calendar_id: str,
    discord_webhook_url: str,
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
        post_to_discord(discord_webhook_url, "📅 No upcoming calendar events.")
        return {"status": "success", "message": "No events found."}

    event_messages = "\n\n".join([format_event(e) for e in events])
    full_message = f"### 📅 Upcoming Google Calendar Events:\n\n{event_messages}"

    post_to_discord(discord_webhook_url, full_message)

    return {"status": "success", "events_sent": len(events)}