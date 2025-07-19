import requests

def share_figma_file(file_key: str, access_token: str, emails: list[str], role: str = "viewer") -> dict:
    headers = {
        "X-Figma-Token": access_token,
        "Content-Type": "application/json"
    }

    url = f"https://api.figma.com/v1/files/{file_key}/share"

    payload = {
        "emails": emails,
        "role": role
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        return {
            "status": "error",
            "message": "Failed to share Figma file",
            "details": response.json()
        }

    return {
        "status": "success",
        "message": f"File shared with: {', '.join(emails)}",
        "role": role
    }