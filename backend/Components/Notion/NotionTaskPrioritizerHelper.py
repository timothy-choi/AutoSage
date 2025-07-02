import requests
from datetime import datetime, timezone
from typing import List, Dict

NOTION_VERSION = "2022-06-28"
NOTION_QUERY_URL = "https://api.notion.com/v1/databases/{}/query"
NOTION_PAGE_URL = "https://api.notion.com/v1/pages/{}"

def fetch_tasks(notion_token: str, database_id: str, max_tasks: int = 10) -> List[Dict]:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    res = requests.post(NOTION_QUERY_URL.format(database_id), headers=headers, json={"page_size": max_tasks})
    if res.status_code != 200:
        raise Exception(f"Failed to fetch tasks: {res.text}")
    return res.json().get("results", [])

def determine_priority(task: Dict) -> str:
    props = task.get("properties", {})
    status = props.get("Status", {}).get("select", {}).get("name", "")
    due_date_str = props.get("Due Date", {}).get("date", {}).get("start", "")

    now = datetime.now(timezone.utc)
    if due_date_str:
        try:
            due = datetime.fromisoformat(due_date_str.replace("Z", "+00:00"))
            days_left = (due - now).days
        except:
            days_left = None
    else:
        days_left = None

    if status.lower() in ["in progress", "not started"]:
        if days_left is not None:
            if days_left <= 1:
                return "High"
            elif days_left <= 3:
                return "Medium"
            else:
                return "Low"
        else:
            return "Medium"
    else:
        return "Low"

def update_priority(notion_token: str, page_id: str, priority: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    body = {
        "properties": {
            "Priority": {
                "select": {
                    "name": priority
                }
            }
        }
    }

    res = requests.patch(NOTION_PAGE_URL.format(page_id), headers=headers, json=body)
    return {
        "page_id": page_id,
        "priority": priority,
        "status": res.status_code,
        "error": None if res.status_code == 200 else res.text
    }

def prioritize_tasks(notion_token: str, database_id: str, max_tasks: int = 10) -> List[Dict]:
    tasks = fetch_tasks(notion_token, database_id, max_tasks)
    results = []
    for task in tasks:
        priority = determine_priority(task)
        result = update_priority(notion_token, task["id"], priority)
        results.append(result)
    return results