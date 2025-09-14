import requests
from typing import Dict, Optional


class BoxFileDownloaderHelper:
    def __init__(self, access_token: str):
        self.base_url = "https://api.box.com/2.0"
        self.download_url = "https://api.box.com/2.0/files/{file_id}/content"
        self.access_token = access_token
        self.headers = {
            "Authorization": f"Bearer {self.access_token}"
        }

    def download_file(self, file_id: str, save_path: Optional[str] = None) -> Dict:
        url = self.download_url.format(file_id=file_id)
        resp = requests.get(url, headers=self.headers, stream=True)

        if resp.status_code == 200:
            if save_path:
                with open(save_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                return {"status": "success", "file_id": file_id, "saved_to": save_path}
            else:
                return {"status": "success", "file_id": file_id, "content": resp.content}
        else:
            return {"error": resp.status_code, "message": resp.text}