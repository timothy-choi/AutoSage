import requests
from datetime import datetime, timedelta
from typing import List

GOOGLE_EVENTS_URL = "https://www.googleapis.com/calendar/v3/calendars/{calendar_id}/events"
NOTION_PAGE_URL = "https://api.notion.com/v1/pages"
NOTION_VERSION = "2022-06-28"

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
        GOOGLE_EVENTS_URL.format(calendar_id=calendar_id),
        headers=headers,
        params=params
    )

    if response.status_code != 200:
        raise Exception(f"Failed to fetch Google Calendar events: {response.text}")

    return response.json().get("items", [])

def create_notion_page(event: dict, notion_token: str, notion_database_id: str) -> dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    start = event.get("start", {}).get("dateTime") or event.get("start", {}).get("date")
    location = event.get("location", "")
    description = event.get("description", "")

    data = {
        "parent": { "database_id": notion_database_id },
        "properties": {
            "Name": {
                "title": [{
                    "text": { "content": event.get("summary", "Untitled Event") }
                }]
            },
            "Start Time": {
                "date": { "start": start }
            },
            "Location": {
                "rich_text": [{
                    "text": { "content": location or "N/A" }
                }]
            },
            "Description": {
                "rich_text": [{
                    "text": { "content": description[:2000] if description else "N/A" }
                }]
            }
        }
    }

    response = requests.post(NOTION_PAGE_URL, json=data, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to create Notion page: {response.text}")
    
    return response.json()

def push_calendar_events_to_notion(
    google_access_token: str,
    calendar_id: str,
    notion_token: str,
    notion_database_id: str,
    hours_ahead: int = 24,
    max_results: int = 10
) -> dict:
    events = fetch_upcoming_events(
        access_token=google_access_token,
        calendar_id=calendar_id,
        hours_ahead=hours_ahead,
        max_results=max_results
    )

    results = []
    for event in events:
        try:
            page = create_notion_page(event, notion_token, notion_database_id)
            results.append({
                "event": event.get("summary"),
                "notion_page_id": page.get("id")
            })
        except Exception as e:
            results.append({
                "event": event.get("summary"),
                "error": str(e)
            })

    return {
        "status": "completed",
        "synced_events": len(results),
        "details": results
    }