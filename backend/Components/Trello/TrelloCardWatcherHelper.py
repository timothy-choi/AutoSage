import requests

def set_card_watch(api_key, token, card_id, watch=True):
    url = f"https://api.trello.com/1/cards/{card_id}/members/me/watched"
    params = {
        "key": api_key,
        "token": token,
        "value": str(watch).lower() 
    }

    response = requests.put(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to set watch status: {response.text}")

    return response.json()