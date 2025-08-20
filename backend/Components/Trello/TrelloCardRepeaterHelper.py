import requests

def repeat_trello_card(card_id: str, target_list_id: str, api_key: str, token: str):
    get_url = f"https://api.trello.com/1/cards/{card_id}"
    params = {"key": api_key, "token": token}
    response = requests.get(get_url, params=params)
    response.raise_for_status()
    card_data = response.json()

    post_url = "https://api.trello.com/1/cards"
    payload = {
        "key": api_key,
        "token": token,
        "idList": target_list_id,
        "name": card_data["name"],
        "desc": card_data.get("desc", ""),
        "due": card_data.get("due"),
        "idLabels": ",".join(card_data.get("idLabels", [])),
        "idMembers": ",".join(card_data.get("idMembers", [])),
    }

    create_response = requests.post(post_url, params=payload)
    create_response.raise_for_status()
    return create_response.json()