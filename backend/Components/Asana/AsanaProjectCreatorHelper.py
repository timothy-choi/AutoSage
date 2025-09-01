import requests
from typing import Dict, Any

class AsanaProjectCreatorHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def create_project(self, workspace_gid: str, name: str, team_gid: str = None, notes: str = None) -> Dict[str, Any]:
        url = f"{self.base_url}/projects"
        payload = {
            "data": {
                "name": name,
                "workspace": workspace_gid
            }
        }
        if team_gid:
            payload["data"]["team"] = team_gid
        if notes:
            payload["data"]["notes"] = notes

        resp = requests.post(url, headers=self.headers, json=payload)

        if resp.status_code == 201:
            return {"success": True, "project": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_projects(self, workspace_gid: str, team_gid: str = None) -> Dict[str, Any]:
        if team_gid:
            url = f"{self.base_url}/teams/{team_gid}/projects"
        else:
            url = f"{self.base_url}/workspaces/{workspace_gid}/projects"

        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "projects": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}