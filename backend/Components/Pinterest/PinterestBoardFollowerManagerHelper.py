import requests

BASE_URL = "https://api.pinterest.com/v5"

def follow_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to follow board: {response.text}")
    return response.json()


def unfollow_board(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to unfollow board: {response.text}")
    return {"message": "Unfollowed successfully"}


def list_board_followers(access_token: str, board_id: str):
    url = f"{BASE_URL}/boards/{board_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to list followers: {response.text}")
    return response.json()