import requests
from typing import Dict

class AsanaProjectDeleterHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def delete_project(self, project_gid: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}"
        resp = requests.delete(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "message": "Project deleted successfully"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def archive_project(self, project_gid: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}"
        payload = {"data": {"archived": True}}
        resp = requests.put(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)

        if resp.status_code == 200:
            return {"success": True, "message": "Project archived successfully", "project": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}