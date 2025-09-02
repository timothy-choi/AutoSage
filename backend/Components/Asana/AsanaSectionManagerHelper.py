import requests
from typing import Dict, List

class AsanaSectionManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_section(self, project_gid: str, name: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}/sections"
        payload = {"data": {"name": name}}
        resp = requests.post(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)

        if resp.status_code == 201:
            return {"success": True, "section": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def update_section(self, section_gid: str, name: str) -> Dict:
        url = f"{self.base_url}/sections/{section_gid}"
        payload = {"data": {"name": name}}
        resp = requests.put(url, headers={**self.headers, "Content-Type": "application/json"}, json=payload)

        if resp.status_code == 200:
            return {"success": True, "section": resp.json().get("data")}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def delete_section(self, section_gid: str) -> Dict:
        url = f"{self.base_url}/sections/{section_gid}"
        resp = requests.delete(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "message": "Section deleted successfully"}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_sections(self, project_gid: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}/sections"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "sections": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}