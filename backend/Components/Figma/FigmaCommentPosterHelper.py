import requests

def post_figma_comment(file_key: str, access_token: str, message: str, client_meta: dict) -> dict:
    url = f"https://api.figma.com/v1/files/{file_key}/comments"

    headers = {
        "X-Figma-Token": access_token,
        "Content-Type": "application/json"
    }

    payload = {
        "message": message,
        "client_meta": client_meta
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to post comment",
            "details": response.json()
        }

    return {
        "status": "success",
        "message": "Comment posted successfully",
        "comment": response.json()
    }