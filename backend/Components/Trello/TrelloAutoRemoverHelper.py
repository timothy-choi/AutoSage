import requests
from datetime import datetime, timezone

def get_cards_from_list(list_id: str, api_key: str, token: str):
    url = f"https://api.trello.com/1/lists/{list_id}/cards"
    params = {"key": api_key, "token": token}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def move_card_to_list(card_id: str, target_list_id: str, api_key: str, token: str):
    url = f"https://api.trello.com/1/cards/{card_id}"
    params = {"key": api_key, "token": token, "idList": target_list_id}
    response = requests.put(url, params=params)
    response.raise_for_status()
    return response.json()

def auto_move_cards(
    source_list_id: str,
    target_list_id: str,
    condition: str,
    api_key: str,
    token: str
):
    moved_cards = []
    cards = get_cards_from_list(source_list_id, api_key, token)

    for card in cards:
        if condition == "past_due" and card.get("due"):
            due_date = datetime.fromisoformat(card["due"].replace("Z", "+00:00"))
            if due_date < datetime.now(timezone.utc):
                result = move_card_to_list(card["id"], target_list_id, api_key, token)
                moved_cards.append(result)

        elif condition == "no_checklists":
            checklists_url = f"https://api.trello.com/1/cards/{card['id']}/checklists"
            params = {"key": api_key, "token": token}
            r = requests.get(checklists_url, params=params)
            r.raise_for_status()
            if not r.json():
                result = move_card_to_list(card["id"], target_list_id, api_key, token)
                moved_cards.append(result)

        elif condition == "no_labels":
            if not card.get("labels"):
                result = move_card_to_list(card["id"], target_list_id, api_key, token)
                moved_cards.append(result)

    return moved_cards