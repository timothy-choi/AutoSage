import requests

BASE_URL = "https://api.pinterest.com/v5"

def create_pin(access_token: str, board_id: str, title: str, description: str, media_url: str, link: str = None):
    url = f"{BASE_URL}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}
    data = {
        "board_id": board_id,
        "title": title,
        "description": description,
        "media_source": {
            "source_type": "image_url",
            "url": media_url
        }
    }
    if link:
        data["link"] = link

    response = requests.post(url, headers=headers, json=data)
    return response.json()

def get_pin(access_token: str, pin_id: str):
    url = f"{BASE_URL}/pins/{pin_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()

def delete_pin(access_token: str, pin_id: str):
    url = f"{BASE_URL}/pins/{pin_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    return {"success": response.status_code == 204}

def list_pins_on_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()