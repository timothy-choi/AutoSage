import requests
from typing import Dict, Any, Optional

class BoxFileVersionManagerHelper:
    def __init__(self, api_base: str, headers: Dict[str, str]):
        self.api_base = api_base
        self.headers = headers

    def list_versions(self, file_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/files/{file_id}/versions"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def promote_version(self, file_id: str, version_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/files/{file_id}/versions/current"
        payload = {"id": version_id}
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def delete_version(self, file_id: str, version_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/files/{file_id}/versions/{version_id}"
        response = requests.delete(url, headers=self.headers)
        return {"status": response.status_code}