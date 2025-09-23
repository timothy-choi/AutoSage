import requests

BASE_URL = "https://api.pinterest.com/v5"

def search_boards(access_token: str, query: str, limit: int = 25):
    url = f"{BASE_URL}/boards/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    params = {
        "query": query,
        "page_size": limit
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to search boards: {response.text}")
    return response.json()