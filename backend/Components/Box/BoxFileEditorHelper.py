import requests
from typing import Dict, Optional


class BoxFileEditorHelper:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.base_url = "https://api.box.com/2.0"
        self.upload_url = "https://upload.box.com/api/2.0/files/{file_id}/content"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def rename_file(self, file_id: str, new_name: str) -> Dict:
        url = f"{self.base_url}/files/{file_id}"
        payload = {"name": new_name}
        resp = requests.put(url, headers=self.headers, json=payload)
        return resp.json()

    def upload_new_version(self, file_id: str, file_path: str) -> Dict:
        url = self.upload_url.format(file_id=file_id)
        with open(file_path, "rb") as f:
            files = {"file": (file_path.split("/")[-1], f)}
            resp = requests.post(url, headers=self.headers, files=files)
        if resp.status_code in (200, 201):
            return resp.json()
        else:
            return {"error": resp.status_code, "message": resp.text}

    def replace_text_in_file(self, file_id: str, text_replacements: Dict[str, str], temp_path: str) -> Dict:
        download_url = f"{self.base_url}/files/{file_id}/content"
        resp = requests.get(download_url, headers=self.headers)
        if resp.status_code != 200:
            return {"error": resp.status_code, "message": resp.text}

        content = resp.content.decode("utf-8")

        for old, new in text_replacements.items():
            content = content.replace(old, new)

        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(content)

        return self.upload_new_version(file_id, temp_path)