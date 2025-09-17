import requests
from typing import Dict, Any, Optional

class BoxFolderCreatorHelper:
    def __init__(self, api_base: str, headers: Dict[str, str]):
        self.api_base = api_base
        self.headers = headers

    def create_folder(self, name: str, parent_id: str = "0") -> Dict[str, Any]:
        url = f"{self.api_base}/folders"
        payload = {
            "name": name,
            "parent": {"id": parent_id}
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def get_folder_info(self, folder_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def list_folder_items(self, folder_id: str, limit: int = 100) -> Dict[str, Any]:
        url = f"{self.api_base}/folders/{folder_id}/items?limit={limit}"
        response = requests.get(url, headers=self.headers)
        return response.json()