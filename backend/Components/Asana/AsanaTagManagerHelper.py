import requests
from typing import Dict, Optional

class AsanaTagManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}

    def create_tag(self, workspace_gid: str, name: str, color: Optional[str] = None) -> Dict:
        url = f"{self.base_url}/tags"
        payload = {"data": {"workspace": workspace_gid, "name": name}}
        if color:
            payload["data"]["color"] = color
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "tag": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def get_tag(self, tag_gid: str) -> Dict:
        url = f"{self.base_url}/tags/{tag_gid}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "tag": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def update_tag(self, tag_gid: str, name: Optional[str] = None, color: Optional[str] = None) -> Dict:
        url = f"{self.base_url}/tags/{tag_gid}"
        data = {}
        if name:
            data["name"] = name
        if color:
            data["color"] = color
        payload = {"data": data}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            return {"success": True, "tag": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def delete_tag(self, tag_gid: str) -> Dict:
        url = f"{self.base_url}/tags/{tag_gid}"
        resp = requests.delete(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "message": "Tag deleted successfully"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def add_tag_to_task(self, task_gid: str, tag_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/addTag"
        payload = {"data": {"tag": tag_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 201]:
            return {"success": True, "result": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def remove_tag_from_task(self, task_gid: str, tag_gid: str) -> Dict:
        url = f"{self.base_url}/tasks/{task_gid}/removeTag"
        payload = {"data": {"tag": tag_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            return {"success": True, "message": "Tag removed from task"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_tags_in_workspace(self, workspace_gid: str) -> Dict:
        url = f"{self.base_url}/workspaces/{workspace_gid}/tags"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200:
            return {"success": True, "tags": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}