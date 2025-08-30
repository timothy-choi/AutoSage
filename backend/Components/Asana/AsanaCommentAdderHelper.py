import requests
from typing import Dict, Any

class AsanaCommentAdderHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def add_comment(self, task_gid: str, text: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/stories"
        data = {"data": {"text": text}}
        resp = requests.post(url, headers=self.headers, json=data)

        if resp.status_code == 201:
            return {"success": True, "comment": resp.json()}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_comments(self, task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/stories"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "comments": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}