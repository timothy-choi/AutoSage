import requests
from collections import Counter
from typing import List, Dict

NOTION_VERSION = "2022-06-28"
NOTION_QUERY_URL = "https://api.notion.com/v1/databases/{}/query"

def fetch_tasks(notion_token: str, database_id: str, max_pages: int = 100) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    response = requests.post(NOTION_QUERY_URL.format(database_id), headers=headers, json={"page_size": max_pages})
    if response.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {response.text}")
    return response.json().get("results", [])

def summarize_status_distribution(tasks: List[Dict], status_property: str = "Status") -> Dict[str, int]:
    counter = Counter()
    for task in tasks:
        props = task.get("properties", {})
        status = props.get(status_property, {}).get("select", {})
        status_name = status.get("name", "Unknown")
        counter[status_name] += 1
    return dict(counter)

def generate_status_report(notion_token: str, database_id: str, status_property: str = "Status", max_pages: int = 100) -> Dict:
    tasks = fetch_tasks(notion_token, database_id, max_pages)
    counts = summarize_status_distribution(tasks, status_property)
    return {
        "status_property": status_property,
        "counts": counts,
        "total_tasks": len(tasks)
    }