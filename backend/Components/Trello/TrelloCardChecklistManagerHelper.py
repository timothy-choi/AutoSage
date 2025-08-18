import requests

def create_checklist(api_key, token, card_id, checklist_name):
    url = f"https://api.trello.com/1/cards/{card_id}/checklists"
    params = {
        "key": api_key,
        "token": token,
        "name": checklist_name
    }

    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Checklist creation failed: {response.text}")

    return response.json()


def add_checklist_item(api_key, token, checklist_id, item_name, checked=False):
    url = f"https://api.trello.com/1/checklists/{checklist_id}/checkItems"
    params = {
        "key": api_key,
        "token": token,
        "name": item_name,
        "checked": str(checked).lower()
    }

    response = requests.post(url, params=params)
    if response.status_code != 200:
        raise Exception(f"Failed to add checklist item: {response.text}")

    return response.json()