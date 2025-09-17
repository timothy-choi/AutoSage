import requests
from typing import Dict, Any

class BoxFolderEditorHelper:
    def __init__(self, api_base: str, headers: Dict[str, str]):
        self.api_base = api_base
        self.headers = headers

    def rename_folder(self, folder_id: str, new_name: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}"
        payload = {"name": new_name}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def move_folder(self, folder_id: str, new_parent_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}"
        payload = {"parent": {"id": new_parent_id}}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def update_description(self, folder_id: str, description: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}"
        payload = {"description": description}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def lock_folder(self, folder_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}/lock"
        response = requests.post(url, headers=self.headers, json={})
        return response.json()

    def unlock_folder(self, folder_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}/lock"
        response = requests.delete(url, headers=self.headers)
        return {"status": response.status_code, "message": "Unlocked" if response.status_code == 204 else response.text}