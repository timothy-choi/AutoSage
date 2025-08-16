import requests

def move_trello_card(api_key, token, card_id, target_list_id):
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {
        "key": api_key,
        "token": token,
        "idList": target_list_id
    }

    response = requests.put(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to move card: {response.text}")

    return response.json()