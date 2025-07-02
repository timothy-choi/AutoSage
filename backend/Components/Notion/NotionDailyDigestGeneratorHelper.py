import requests
from datetime import datetime, timedelta, timezone
from typing import List, Dict

NOTION_VERSION = "2022-06-28"
NOTION_QUERY_URL = "https://api.notion.com/v1/databases/{}/query"

def fetch_recent_entries(notion_token: str, database_id: str, hours_back: int = 24, max_items: int = 25) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    since = datetime.now(timezone.utc) - timedelta(hours=hours_back)

    payload = {
        "page_size": max_items,
        "filter": {
            "timestamp": "last_edited_time",
            "last_edited_time": {
                "on_or_after": since.isoformat()
            }
        }
    }

    response = requests.post(NOTION_QUERY_URL.format(database_id), headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch recent Notion entries: {response.text}")
    return response.json().get("results", [])

def format_digest(entries: List[Dict]) -> str:
    if not entries:
        return "No updates in the last 24 hours."

    digest_lines = ["📬 **Daily Digest** – Recent Notion Updates:\n"]
    for entry in entries:
        props = entry.get("properties", {})
        title_obj = props.get("Name", {}).get("title", [])
        title = title_obj[0]["plain_text"] if title_obj else "(Untitled)"
        last_edited = entry.get("last_edited_time", "Unknown time")
        digest_lines.append(f"- {title} (edited: {last_edited[:10]})")

    return "\n".join(digest_lines)

def generate_notion_daily_digest(notion_token: str, database_id: str, hours_back: int = 24, max_items: int = 25) -> Dict:
    entries = fetch_recent_entries(notion_token, database_id, hours_back, max_items)
    digest = format_digest(entries)
    return {
        "digest": digest,
        "count": len(entries),
        "range_hours": hours_back
    }