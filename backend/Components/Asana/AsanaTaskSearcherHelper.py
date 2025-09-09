import requests
from typing import Dict, Optional

class AsanaTaskSearcherHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def search_tasks_in_project(self, project_gid: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}/tasks"
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            return {"success": True, "tasks": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def search_tasks_in_workspace(self, workspace_gid: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}/tasks/search"
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            return {"success": True, "tasks": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def search_tasks_by_assignee(self, workspace_gid: str, assignee_gid: str, params: Optional[Dict] = None) -> Dict:
        if params is None:
            params = {}
        params["assignee.any"] = assignee_gid
        url = f"{self.base_url}/workspaces/{workspace_gid}/tasks/search"
        resp = requests.get(url, headers=self.headers, params=params)
        if resp.status_code == 200:
            return {"success": True, "tasks": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}