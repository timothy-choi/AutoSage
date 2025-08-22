import requests

def add_label_to_card(api_key, token, card_id, label_id):
    url = f"https://api.trello.com/1/cards/{card_id}/idLabels"
    params = {
        "key": api_key,
        "token": token,
        "value": label_id
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()