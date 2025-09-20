import requests

BASE_URL = "https://api.box.com/2.0"

def create_tag(access_token: str, tag_name: str):
    url = f"{BASE_URL}/tags"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"name": tag_name}
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def delete_tag(access_token: str, tag_id: str):
    url = f"{BASE_URL}/tags/{tag_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    return {"success": response.status_code == 204}

def list_tags(access_token: str, file_id: str):
    url = f"{BASE_URL}/files/{file_id}/tags"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def attach_tag(access_token: str, file_id: str, tag_name: str):
    url = f"{BASE_URL}/files/{file_id}/tags"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"op": "add", "path": "/tags/-", "value": tag_name}
    response = requests.put(url, headers=headers, json=[data])
    return response.json()

def detach_tag(access_token: str, file_id: str, tag_name: str):
    url = f"{BASE_URL}/files/{file_id}/tags"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"op": "remove", "path": f"/tags/{tag_name}"}
    response = requests.put(url, headers=headers, json=[data])
    return response.json()