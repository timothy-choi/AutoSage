import requests

BASE_URL = "https://api.pinterest.com/v5"

def repin(access_token: str, board_id: str, parent_pin_id: str, title: str = None, description: str = None):
    url = f"{BASE_URL}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    data = {
        "board_id": board_id,
        "parent_pin_id": parent_pin_id,
    }
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()