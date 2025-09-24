import requests

BASE_URL = "https://api.pinterest.com/v5"

def create_comment(access_token: str, pin_id: str, text: str):
    url = f"{BASE_URL}/pins/{pin_id}/comments"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"text": text}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to create comment: {response.text}")
    return response.json()


def list_comments(access_token: str, pin_id: str, limit: int = 25):
    url = f"{BASE_URL}/pins/{pin_id}/comments"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list comments: {response.text}")
    return response.json()


def delete_comment(access_token: str, pin_id: str, comment_id: str):
    url = f"{BASE_URL}/pins/{pin_id}/comments/{comment_id}"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to delete comment: {response.text}")
    return {"message": "Comment deleted successfully"}