import requests
from typing import Dict


class BoxFileMoverHelper:
    def __init__(self, access_token: str):
        self.base_url = "https://api.box.com/2.0"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def move_file(self, file_id: str, new_parent_id: str) -> Dict:
        url = f"{self.base_url}/files/{file_id}"
        payload = {"parent": {"id": new_parent_id}}
        resp = requests.put(url, headers=self.headers, json=payload)
        if resp.status_code in (200, 201):
            return resp.json()
        else:
            return {"error": resp.status_code, "message": resp.text}