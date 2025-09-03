import requests
from typing import Dict, Optional

class AsanaTaskManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_task(self, workspace_gid: str, name: str, assignee: Optional[str] = None, notes: Optional[str] = None, projects: Optional[list] = None) -> Dict:
        url = f"{self.base_url}/tasks"
        payload = {"data": {"workspace": workspace_gid, "name": name}}
        if assignee:
            payload["data"]["assignee"] = assignee
        if notes:
            payload["data"]["notes"] = notes
        if projects:
            payload["data"]["projects"] = projects

        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "task": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_task(self, task_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "task": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def update_task(self, task_gid: str, updates: Dict) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        payload = {"data": updates}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            return {"success": True, "task": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def delete_task(self, task_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "message": "Task deleted successfully"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def complete_task(self, task_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        payload = {"data": {"completed": True}}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            return {"success": True, "task": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def assign_task(self, task_gid: str, user_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}"
        payload = {"data": {"assignee": user_gid}}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            return {"success": True, "task": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def move_task_to_section(self, task_gid: str, section_gid: str) -> Dict:
        url = f"{self.base_url}/sections/{section_gid}/addTask"
        payload = {"data": {"task": task_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "result": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}