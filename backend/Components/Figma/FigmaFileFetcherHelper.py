import requests
from typing import Optional

FIGMA_API_BASE = "https://api.figma.com/v1"

class FigmaFileFetcher:
    def __init__(self, access_token: str):
        self.access_token = access_token

    def fetch_file(self, file_key: str) -> dict:
        url = f"{FIGMA_API_BASE}/files/{file_key}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    def fetch_file_nodes(self, file_key: str, node_ids: list[str]) -> dict:
        url = f"{FIGMA_API_BASE}/files/{file_key}/nodes"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "ids": ",".join(node_ids)
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_file_images(self, file_key: str, ids: list[str], scale: float = 1.0, format: str = "png") -> dict:
        url = f"{FIGMA_API_BASE}/images/{file_key}"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        params = {
            "ids": ",".join(ids),
            "scale": scale,
            "format": format
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()