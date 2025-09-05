import requests
from typing import Dict

class AsanaFollowerManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def add_follower(self, task_gid: str, user_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/addFollowers"
        payload = {"data": {"followers": [user_gid]}}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "followers": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def remove_follower(self, task_gid: str, user_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/removeFollowers"
        payload = {"data": {"followers": [user_gid]}}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "message": "Follower removed"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_followers(self, task_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/followers"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "followers": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}