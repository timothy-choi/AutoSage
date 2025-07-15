import requests
from typing import Optional, List
from datetime import datetime

DROPBOX_TEAM_LOG_URL = "https://api.dropboxapi.com/2/team_log/get_events"

def fetch_dropbox_team_activity(
    team_access_token: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    limit: int = 100
) -> List[dict]:
    headers = {
        "Authorization": f"Bearer {team_access_token}",
        "Content-Type": "application/json"
    }

    body = {
        "limit": min(limit, 1000)
    }

    if start_time or end_time:
        body["time"] = {}
        if start_time:
            body["time"]["start_time"] = start_time
        if end_time:
            body["time"]["end_time"] = end_time

    response = requests.post(DROPBOX_TEAM_LOG_URL, headers=headers, json=body)
    if response.status_code != 200:
        raise Exception(f"Dropbox team log API error: {response.text}")

    data = response.json()
    events = data.get("events", [])

    parsed_events = []
    for event in events:
        parsed_events.append({
            "event_type": event.get("event_type", {}).get(".tag"),
            "event_category": event.get("category", {}).get(".tag"),
            "timestamp": event.get("timestamp"),
            "actor": event.get("actor", {}).get("display_name", "Unknown"),
            "details": event.get("details", {})
        })

    return parsed_events