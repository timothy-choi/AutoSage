import requests

def clone_trello_board(api_key, token, source_board_id, name=None, keep_cards=True, keep_lists=True, keep_members=False):
    url = "https://api.trello.com/1/boards/"

    params = {
        "key": api_key,
        "token": token,
        "idBoardSource": source_board_id,
        "name": name or "Cloned Board",
        "keepFromSource": ",".join([
            part for part, keep in {
                "cards": keep_cards,
                "lists": keep_lists,
                "members": keep_members
            }.items() if keep
        ])
    }

    response = requests.post(url, params=params)

    if response.status_code != 200:
        raise Exception(f"Failed to clone board: {response.text}")

    return response.json()