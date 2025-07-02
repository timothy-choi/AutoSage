import requests
from datetime import datetime, timedelta
from typing import Dict

NOTION_VERSION = "2022-06-28"
NOTION_CREATE_PAGE_URL = "https://api.notion.com/v1/pages"

def get_next_due_date(frequency: str) -> str:
    now = datetime.now()
    if frequency == "daily":
        return (now + timedelta(days=1)).isoformat()
    elif frequency == "weekly":
        return (now + timedelta(weeks=1)).isoformat()
    elif frequency == "monthly":
        return (now.replace(day=1) + timedelta(days=32)).replace(day=1).isoformat()
    else:
        raise ValueError("Unsupported frequency")

def create_recurring_task(notion_token: str, database_id: str, template: Dict, frequency: str) -> Dict:
    headers = {
        "Authorization": f"Bearer {notion_token}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }

    due_date = get_next_due_date(frequency)

    # Override template with new due date if "Due Date" property exists
    if "Due Date" in template:
        template["Due Date"] = {
            "date": {
                "start": due_date
            }
        }

    payload = {
        "parent": { "database_id": database_id },
        "properties": template
    }

    response = requests.post(NOTION_CREATE_PAGE_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to create recurring task: {response.text}")

    return {
        "status": "success",
        "task_id": response.json()["id"],
        "due_date": due_date,
        "frequency": frequency
    }