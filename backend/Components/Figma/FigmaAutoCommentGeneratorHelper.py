import requests

def generate_auto_comment(file_key: str, access_token: str, comment: str, position: dict, client_meta: dict = None) -> dict:
    headers = {
        "X-Figma-Token": access_token,
        "Content-Type": "application/json"
    }

    payload = {
        "message": comment,
        "client_meta": position
    }

    if client_meta:
        payload["client_meta"].update(client_meta)

    url = f"https://api.figma.com/v1/files/{file_key}/comments"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to post comment.",
            "details": response.json()
        }

    return {
        "status": "success",
        "comment_id": response.json().get("id"),
        "created_at": response.json().get("created_at")
    }