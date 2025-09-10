import requests
from typing import Dict, List, Optional


class AsanaCustomFieldManagerHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def list_custom_fields(self, workspace_gid: str) -> List[Dict]:
        url = f"{self.base_url}/workspaces/{workspace_gid}/custom_fields"
        resp = requests.get(url, headers=self.headers)
        return resp.json().get("data", []) if resp.status_code == 200 else []

    def create_custom_field(
        self,
        workspace_gid: str,
        name: str,
        field_type: str,
        enum_options: Optional[List[str]] = None
    ) -> Dict:
        url = f"{self.base_url}/custom_fields"
        payload = {
            "data": {
                "workspace": workspace_gid,
                "name": name,
                "type": field_type
            }
        }
        if field_type == "enum" and enum_options:
            payload["data"]["enum_options"] = [{"name": e} for e in enum_options]

        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def update_custom_field(self, field_gid: str, updates: Dict) -> Dict:
        url = f"{self.base_url}/custom_fields/{field_gid}"
        payload = {"data": updates}
        resp = requests.put(url, headers=self.headers, json=payload)
        return resp.json()

    def delete_custom_field(self, field_gid: str) -> Dict:
        url = f"{self.base_url}/custom_fields/{field_gid}"
        resp = requests.delete(url, headers=self.headers)
        return {"success": resp.status_code == 200, "status": resp.status_code}

    def add_custom_field_to_project(self, project_gid: str, field_gid: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}/addCustomFieldSetting"
        payload = {"data": {"custom_field": field_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    def remove_custom_field_from_project(self, project_gid: str, field_gid: str) -> Dict:
        url = f"{self.base_url}/projects/{project_gid}/removeCustomFieldSetting"
        payload = {"data": {"custom_field": field_gid}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()