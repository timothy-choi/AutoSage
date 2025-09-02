import requests
from typing import Dict

class AsanaWorkspaceManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def list_workspaces(self) -> Dict:
        url = f"{self.base_url}/workspaces"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "workspaces": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_workspace(self, workspace_gid: str) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "workspace": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def update_workspace(self, workspace_gid: str, name: str) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}"
        payload = {"data": {"name": name}}
        resp = requests.put(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)

        if resp.status_code == 200:
            return {"success": True, "workspace": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_users_in_workspace(self, workspace_gid: str) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}/users"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "users": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}