import requests
from typing import Dict, Any, List, Optional

class AsanaTaskCreatorHelper:
    def __init__(self, token: str, workspace_gid: str, project_gid: Optional[str] = None):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        self.workspace_gid = workspace_gid
        self.project_gid = project_gid

    def create_task(self, name: str, notes: str = "", assignee: Optional[str] = None,
                    due_date: Optional[str] = None, tags: Optional[List[str]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks"
        payload = {
            "data": {
                "workspace": self.workspace_gid,
                "name": name,
                "notes": notes
            }
        }
        if self.project_gid:
            payload["data"]["projects"] = [self.project_gid]
        if assignee:
            payload["data"]["assignee"] = assignee
        if due_date:
            payload["data"]["due_on"] = due_date
        if tags:
            payload["data"]["tags"] = tags

        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def list_projects(self) -> Dict[str, Any]:
        url = f"{self.base_url}/projects"
        resp = requests.get(url, headers=self.headers, params={"workspace": self.workspace_gid})
        return resp.json()

    def list_users(self) -> Dict[str, Any]:
        url = f"{self.base_url}/users"
        resp = requests.get(url, headers=self.headers, params={"workspace": self.workspace_gid})
        return resp.json()