import requests
from typing import Dict, List
from datetime import datetime

class AsanaCalendarSyncerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def fetch_upcoming_tasks(self, project_gid: str, limit: int = 20) -> List[Dict]:
        url = f"{self.base_url}/projects/{project_gid}/tasks"
        params = {"limit": limit, "opt_fields": "name,due_on,permalink_url,assignee"}
        resp = requests.get(url, headers=self.headers, params=params)

        if resp.status_code == 200:
            tasks = [
                t for t in resp.json().get("data", [])
                if t.get("due_on") is not None
            ]
            return tasks
        return []

    def convert_to_calendar_events(self, tasks: List[Dict]) -> List[Dict]:
        events = []
        for t in tasks:
            event = {
                "title": t.get("name"),
                "start": t.get("due_on"),
                "end": t.get("due_on"),
                "url": t.get("permalink_url"),
                "assignee": t.get("assignee", {}).get("name") if t.get("assignee") else None
            }
            events.append(event)
        return events