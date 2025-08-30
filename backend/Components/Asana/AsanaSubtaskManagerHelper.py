import requests
from typing import Dict, Any, List

class AsanaSubtaskManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_subtask(self, parent_task_gid: str, name: str, notes: str = "") -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{parent_task_gid}/subtasks"
        data = {"data": {"name": name, "notes": notes}}
        resp = requests.post(url, headers=self.headers, json=data)

        if resp.status_code == 201:
            return {"success": True, "subtask": resp.json()}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_subtasks(self, parent_task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{parent_task_gid}/subtasks"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "subtasks": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def update_subtask(self, subtask_gid: str, updates: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{subtask_gid}"
        data = {"data": updates}
        resp = requests.put(url, headers=self.headers, json=data)

        if resp.status_code == 200:
            return {"success": True, "updated_subtask": resp.json()}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def delete_subtask(self, subtask_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{subtask_gid}"
        resp = requests.delete(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "message": f"Subtask {subtask_gid} deleted."}
        return {"success": False, "status": resp.status_code, "details": resp.text}