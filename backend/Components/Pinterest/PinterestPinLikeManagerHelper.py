import requests

BASE_URL = "https://api.pinterest.com/v5"

def like_pin(access_token: str, pin_id: str):
    url = f"{BASE_URL}/pins/{pin_id}/likes"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.post(url, headers=headers)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to like pin: {response.text}")
    return response.json()


def unlike_pin(access_token: str, pin_id: str):
    url = f"{BASE_URL}/pins/{pin_id}/likes"
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to unlike pin: {response.text}")
    return {"message": "Pin unliked successfully"}


def list_pin_likes(access_token: str, pin_id: str, limit: int = 25):
    url = f"{BASE_URL}/pins/{pin_id}/likes"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list likes: {response.text}")
    return response.json()