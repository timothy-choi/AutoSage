import requests

BASE_URL = "https://api.pinterest.com/v5"

def repin_pin(access_token: str, pin_id: str, board_id: str, note: str = None):
    url = f"{BASE_URL}/pins"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "board_id": board_id,
        "parent_pin_id": pin_id
    }
    if note:
        payload["note"] = note

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to repin pin: {response.text}")
    return response.json()


def bulk_repin(access_token: str, pin_id: str, board_ids: list[str], note: str = None):
    results = []
    for board_id in board_ids:
        try:
            result = repin_pin(access_token, pin_id, board_id, note)
            results.append({"board_id": board_id, "status": "success", "data": result})
        except Exception as e:
            results.append({"board_id": board_id, "status": "failed", "error": str(e)})
    return results