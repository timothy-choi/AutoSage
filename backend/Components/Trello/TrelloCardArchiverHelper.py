import requests

def archive_trello_card(api_key, token, card_id):
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": api_key,
        "token": token,
        "closed": "true"
    }

    response = requests.put(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to archive card: {response.text}")

    return response.json()