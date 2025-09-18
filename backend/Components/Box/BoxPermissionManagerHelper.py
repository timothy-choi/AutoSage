import requests
from typing import Dict, Any

class BoxPermissionManagerHelper:
    def __init__(self, api_base: str, headers: Dict[str, str]):
        self.api_base = api_base
        self.headers = headers

    def add_collaborator(self, item_id: str, item_type: str, user_login: str, role: str) -> Dict[str, Any]:
        url = f"{self.api_base}/{item_type}/{item_id}/collaborations"
        payload = {
            "accessible_by": {"login": user_login, "type": "user"},
            "role": role
        }
        response = requests.post(url, headers=self.headers, json=payload)
        return response.json()

    def remove_collaborator(self, collaboration_id: str) -> Dict[str, Any]:
        url = f"{self.api_base}/collaborations/{collaboration_id}"
        response = requests.delete(url, headers=self.headers)
        return {"status": response.status_code, "message": "Removed" if response.status_code == 204 else response.text}

    def update_collaborator_role(self, collaboration_id: str, new_role: str) -> Dict[str, Any]:
        url = f"{self.api_base}/collaborations/{collaboration_id}"
        payload = {"role": new_role}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def list_collaborators(self, item_id: str, item_type: str) -> Dict[str, Any]:
        url = f"{self.api_base}/{item_type}/{item_id}/collaborations"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def set_shared_link(self, item_id: str, item_type: str, access: str = "open") -> Dict[str, Any]:
        url = f"{self.api_base}/{item_type}/{item_id}"
        payload = {"shared_link": {"access": access}}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()

    def revoke_shared_link(self, item_id: str, item_type: str) -> Dict[str, Any]:
        url = f"{self.api_base}/{item_type}/{item_id}"
        payload = {"shared_link": None}
        response = requests.put(url, headers=self.headers, json=payload)
        return response.json()