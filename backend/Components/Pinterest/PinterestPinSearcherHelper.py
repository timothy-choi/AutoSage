import requests

BASE_URL = "https://api.pinterest.com/v5"

def search_pins(access_token: str, query: str, board_id: str = None, limit: int = 25):
    url = f"{BASE_URL}/pins/search"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    params = {
        "query": query,
        "page_size": limit
    }
    if board_id:
        params["board_id"] = board_id

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to search pins: {response.text}")
    return response.json()