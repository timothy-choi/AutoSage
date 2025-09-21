import requests

BASE_URL = "https://api.pinterest.com/v5"

def update_pin(access_token: str, pin_id: str, title: str = None, description: str = None, link: str = None, board_id: str = None):
    url = f"{BASE_URL}/pins/{pin_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    data = {}
    if title:
        data["title"] = title
    if description:
        data["description"] = description
    if link:
        data["link"] = link
    if board_id:
        data["board_id"] = board_id
    
    response = requests.patch(url, headers=headers, json=data)
    return response.json()