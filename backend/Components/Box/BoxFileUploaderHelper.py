import requests
from typing import Dict, Optional


class BoxFileUploaderHelper:
    def __init__(self, access_token: str):
        self.base_url = "https://upload.box.com/api/2.0"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def upload_file(self, folder_id: str, file_path: str) -> Dict:
        url = f"{self.base_url}/files/content"
        with open(file_path, "rb") as f:
            files = {
                "attributes": (
                    None,
                    f'{{"name":"{file_path.split("/")[-1]}","parent":{"id":"{folder_id}"}}}',
                    "application/json"
                ),
                "file": (file_path.split("/")[-1], f, "application/octet-stream")
            }
            resp = requests.post(url, headers=self.headers, files=files)

        if resp.status_code in (200, 201):
            return resp.json()
        else:
            return {"error": resp.status_code, "message": resp.text}