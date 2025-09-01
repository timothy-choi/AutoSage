import requests
from typing import Dict, Any

class AsanaProjectEditorHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def update_project(self, project_gid: str, fields: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/projects/{project_gid}"
        payload = {"data": fields}

        resp = requests.put(url, headers=self.headers, json=payload)

        if resp.status_code == 200:
            return {"success": True, "project": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_project(self, project_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/projects/{project_gid}"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "project": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}