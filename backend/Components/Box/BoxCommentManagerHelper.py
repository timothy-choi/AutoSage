import requests

BASE_URL = "https://api.box.com/2.0"

def create_comment(access_token: str, file_id: str, message: str):
    url = f"{BASE_URL}/comments"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "item": {"type": "file", "id": file_id},
        "message": message
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_comment(access_token: str, comment_id: str):
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def list_comments(access_token: str, file_id: str):
    url = f"{BASE_URL}/files/{file_id}/comments"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def update_comment(access_token: str, comment_id: str, message: str):
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"message": message}
    response = requests.put(url, headers=headers, json=data)
    return response.json()

def delete_comment(access_token: str, comment_id: str):
    url = f"{BASE_URL}/comments/{comment_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    return {"success": response.status_code == 204}