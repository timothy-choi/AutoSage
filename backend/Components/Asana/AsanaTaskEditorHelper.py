import requests
from typing import Dict, Any, Optional

class AsanaTaskEditorHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def update_task(
        self,
        task_gid: str,
        name: Optional[str] = None,
        notes: Optional[str] = None,
        assignee: Optional[str] = None,
        due_date: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}"
        data = {"data": {}}

        if name:
            data["data"]["name"] = name
        if notes:
            data["data"]["notes"] = notes
        if assignee:
            data["data"]["assignee"] = assignee
        if due_date:
            data["data"]["due_on"] = due_date
        if completed is not None:
            data["data"]["completed"] = completed

        resp = requests.put(url, headers=self.headers, json=data)
        return resp.json()

    def add_project(self, task_gid: str, project_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/addProject"
        payload = {"data": {"project": project_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def remove_project(self, task_gid: str, project_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/removeProject"
        payload = {"data": {"project": project_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def add_tag(self, task_gid: str, tag_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/addTag"
        payload = {"data": {"tag": tag_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def remove_tag(self, task_gid: str, tag_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/removeTag"
        payload = {"data": {"tag": tag_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()