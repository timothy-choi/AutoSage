import requests
from typing import Dict, List
import fnmatch

class BoxFileCopierHelper:
    def __init__(self, access_token: str):
        self.base_url = "https://api.box.com/2.0"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def copy_file(self, file_id: str, new_parent_id: str) -> Dict:
        url = f"{self.base_url}/files/{file_id}/copy"
        payload = {"parent": {"id": new_parent_id}}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.status_code, "message": resp.text}

    def copy_file_and_rename(self, file_id: str, new_parent_id: str, new_name: str) -> Dict:
        url = f"{self.base_url}/files/{file_id}/copy"
        payload = {"parent": {"id": new_parent_id}, "name": new_name}
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json() if resp.status_code in (200, 201) else {"error": resp.status_code, "message": resp.text}

    def batch_copy_files(self, file_ids: List[str], new_parent_id: str) -> List[Dict]:
        results = []
        for fid in file_ids:
            results.append(self.copy_file(fid, new_parent_id))
        return results

    def copy_files_by_pattern(self, folder_id: str, pattern: str, new_parent_id: str) -> List[Dict]:
        url = f"{self.base_url}/folders/{folder_id}/items"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return [{"error": resp.status_code, "message": resp.text}]
        items = resp.json().get("entries", [])
        matching_files = [item for item in items if item["type"] == "file" and fnmatch.fnmatch(item["name"], pattern)]
        return self.batch_copy_files([f["id"] for f in matching_files], new_parent_id)

    def preview_copy_by_pattern(self, folder_id: str, pattern: str) -> List[str]:
        url = f"{self.base_url}/folders/{folder_id}/items"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code != 200:
            return []
        items = resp.json().get("entries", [])
        return [item["name"] for item in items if item["type"] == "file" and fnmatch.fnmatch(item["name"], pattern)]