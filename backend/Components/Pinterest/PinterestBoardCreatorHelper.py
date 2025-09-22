import requests

BASE_URL = "https://api.pinterest.com/v5"

def create_board(access_token: str, name: str, description: str = None, privacy: str = "PUBLIC"):
    url = f"{BASE_URL}/boards"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {"name": name, "privacy": privacy}
    if description:
        data["description"] = description

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def delete_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    return {"success": response.status_code == 204}

def list_boards(access_token: str):
    url = f"{BASE_URL}/boards"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()