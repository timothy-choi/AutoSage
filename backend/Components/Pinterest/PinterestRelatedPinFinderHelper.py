import requests

BASE_URL = "https://api.pinterest.com/v5"

def find_related_pins(access_token: str, pin_id: str, limit: int = 25, media_type: str = None):
    url = f"{BASE_URL}/pins/{pin_id}/related"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}
    if media_type:
        params["media_type"] = media_type

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch related pins: {response.text}")
    return response.json()


def bulk_find_related_pins(access_token: str, pin_ids: list[str], limit: int = 10):
    results = {}
    for pin_id in pin_ids:
        try:
            results[pin_id] = find_related_pins(access_token, pin_id, limit)
        except Exception as e:
            results[pin_id] = {"error": str(e)}
    return results


def get_recommended_pins(access_token: str, limit: int = 25):
    url = f"{BASE_URL}/pins/recommended"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch recommended pins: {response.text}")
    return response.json()