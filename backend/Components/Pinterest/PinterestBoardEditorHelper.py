import requests

BASE_URL = "https://api.pinterest.com/v5/boards"

def edit_board(access_token: str, board_id: str, name: str = None, description: str = None, privacy: str = None):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {}
    if name:
        payload["name"] = name
    if description:
        payload["description"] = description
    if privacy:
        payload["privacy"] = privacy 

    url = f"{BASE_URL}/{board_id}"
    response = requests.patch(url, headers=headers, json=payload)

    if response.status_code not in (200, 201):
        raise Exception(f"Failed to edit board: {response.text}")

    return response.json()


def delete_board(access_token: str, board_id: str):
    headers = {
        "Authorization": f"Bearer {access_token}",
    }

    url = f"{BASE_URL}/{board_id}"
    response = requests.delete(url, headers=headers)

    if response.status_code != 204:
        raise Exception(f"Failed to delete board: {response.text}")

    return {"message": "Board deleted successfully"}