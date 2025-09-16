import requests

BOX_API_BASE = "https://api.box.com/2.0"

def preview_file(file_id: str, access_token: str):
    url = f"{BOX_API_BASE}/files/{file_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_data = response.json()
        if "expiring_embed_link" in file_data:
            return {"preview_url": file_data["expiring_embed_link"]["url"]}
        return {"message": "Preview not available for this file type."}
    return {"error": response.json()}