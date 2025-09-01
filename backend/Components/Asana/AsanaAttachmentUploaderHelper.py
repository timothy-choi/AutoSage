import requests
from typing import Dict, Any

class AsanaAttachmentUploaderHelper:
    def __init__(self, token: str):
        self.token = token
        self.base_url = "https://app.asana.com/api/1.0"
        self.headers = {
            "Authorization": f"Bearer {self.token}"
        }

    def upload_attachment(self, task_gid: str, file_path: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/attachments"

        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(url, headers=self.headers, files=files)

        if resp.status_code == 201:
            return {"success": True, "attachment": resp.json()}
        return {"success": False, "status": resp.status_code, "details": resp.text}

    def list_attachments(self, task_gid: str) -> Dict[str, Any]:
        url = f"{self.base_url}/tasks/{task_gid}/attachments"
        resp = requests.get(url, headers=self.headers)

        if resp.status_code == 200:
            return {"success": True, "attachments": resp.json().get("data", [])}
        return {"success": False, "status": resp.status_code, "details": resp.text}