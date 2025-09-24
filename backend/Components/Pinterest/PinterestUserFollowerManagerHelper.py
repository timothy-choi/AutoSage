import requests

BASE_URL = "https://api.pinterest.com/v5"

def follow_user(access_token: str, user_id: str):
    url = f"{BASE_URL}/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    if response.status_code not in (200, 201):
        raise Exception(f"Failed to follow user: {response.text}")
    return response.json()


def unfollow_user(access_token: str, user_id: str):
    url = f"{BASE_URL}/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.delete(url, headers=headers)
    if response.status_code != 204:
        raise Exception(f"Failed to unfollow user: {response.text}")
    return {"message": "Unfollowed successfully"}


def list_user_followers(access_token: str, user_id: str, limit: int = 25):
    url = f"{BASE_URL}/users/{user_id}/followers"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list followers: {response.text}")
    return response.json()


def list_user_following(access_token: str, user_id: str, limit: int = 25):
    url = f"{BASE_URL}/users/{user_id}/following"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"page_size": limit}
    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to list following: {response.text}")
    return response.json()