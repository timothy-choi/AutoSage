import requests
from typing import Dict, List, Optional

NOTION_QUERY_API = "https://api.notion.com/v1/databases/{}/query"
NOTION_VERSION = "2022-06-28"
GOOGLE_CALENDAR_API = "https://www.googleapis.com/calendar/v3/calendars/{}/events"

def fetch_notion_events(notion_token: str, database_id: str, max_events: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    response = requests.post(NOTION_QUERY_API.format(database_id), headers=headers, json={"page_size": max_events})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch Notion data: {response.text}")
    return response.json().get("results", [])

def extract_event_data(notion_entry: Dict) -> Optional[Dict]:
    props = notion_entry.get("properties", {})
    title_prop = props.get("Name") or props.get("Title")
    date_prop = props.get("Date") or props.get("Due") or props.get("Time")

    title = title_prop.get("title", [{}])[0].get("plain_text") if title_prop else "Untitled"
    if not date_prop or "date" not in date_prop:
        return None
    date_range = date_prop["date"]
    start = date_range.get("start")
    end = date_range.get("end") or start  # all-day event fallback

    return {
        "summary": title,
        "start": {"dateTime": start} if "T" in start else {"date": start},
        "end": {"dateTime": end} if "T" in end else {"date": end}
    }

def create_google_calendar_event(google_token: str, calendar_id: str, event_data: Dict) -> Dict:
    headers = {
        "Authorization": f"Bearer {google_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(GOOGLE_CALENDAR_API.format(calendar_id), headers=headers, json=event_data)
    return {
        "status": response.status_code,
        "summary": event_data.get("summary"),
        "calendar_link": response.json().get("htmlLink") if response.status_code == 200 else None,
        "error": None if response.status_code == 200 else response.text
    }

def sync_notion_to_google_calendar(notion_token: str, database_id: str, google_token: str, calendar_id: str, max_events: int = 10) -> List[Dict]:
    notion_events = fetch_notion_events(notion_token, database_id, max_events)
    results = []
    for entry in notion_events:
        event_data = extract_event_data(entry)
        if event_data:
            result = create_google_calendar_event(google_token, calendar_id, event_data)
            results.append(result)
    return results