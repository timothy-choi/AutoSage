import requests
from typing import Dict

class AsanaUserManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def list_users(self, workspace_gid: str) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}/users"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "users": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_user(self, user_gid: str) -> Dict:
        url = f"{self.base_url}/users/{user_gid}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "user": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_current_user(self) -> Dict:
        url = f"{self.base_url}/users/me"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "user": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}