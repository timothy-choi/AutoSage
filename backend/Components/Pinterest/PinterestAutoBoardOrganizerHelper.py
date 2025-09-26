import requests

BASE_URL = "https://api.pinterest.com/v5"


def reorder_pins_in_board(access_token: str, board_id: str, pin_ids: list[str]):
    url = f"{BASE_URL}/boards/{board_id}/pins/reorder"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"pin_ids": pin_ids}

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to reorder pins: {response.text}")
    return response.json()


def move_pin_to_board(access_token: str, pin_id: str, new_board_id: str):
    url = f"{BASE_URL}/pins/{pin_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"board_id": new_board_id}

    response = requests.patch(url, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"Failed to move pin: {response.text}")
    return response.json()


def clean_old_pins(access_token: str, board_id: str, limit: int = 50):
    url = f"{BASE_URL}/boards/{board_id}/pins"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch pins: {response.text}")
    pins = response.json().get("items", [])

    results = []
    for pin in pins:
        pin_id = pin.get("id")
        try:
            delete_url = f"{BASE_URL}/pins/{pin_id}"
            delete_resp = requests.delete(delete_url, headers=headers)
            if delete_resp.status_code == 204:
                results.append({"pin_id": pin_id, "status": "deleted"})
            else:
                results.append({"pin_id": pin_id, "status": "failed", "error": delete_resp.text})
        except Exception as e:
            results.append({"pin_id": pin_id, "status": "failed", "error": str(e)})

    return results